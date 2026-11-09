# SPDX-License-Identifier: MIT
"""GraphTools adapter backed exclusively by an already scoped packet."""
import json
from pathlib import Path
from graph.tools import GraphTools, arguments
from teacher.worker import load_blob


class PacketTimeline:
    def __init__(self, packet, manifest):
        self.packet = packet
        self.manifest = manifest
        self.cache = {}

    def parents(self, sha):
        if sha == self.manifest['task_sha']:
            return self.manifest['task_parents']
        if sha not in self.manifest['graphs']:
            raise ValueError('Graph commit outside strict-ancestor packet')
        return self.manifest['commits'][sha]['parents']

    def authorize(self, sha, cutoff):
        if cutoff != self.manifest['task_sha'] or sha not in self.manifest['graphs']:
            raise ValueError('Graph commit outside strict-ancestor packet')

    def snapshot(self, sha):
        if sha not in self.cache:
            self.cache[sha] = json.loads(load_blob(self.packet,self.manifest['graphs'][sha]['snapshot']))
        return self.cache[sha]

    def history(self, symbol, commit):
        allowed = set()
        pending = [commit]
        while pending:
            sha = pending.pop()
            if sha not in allowed:
                allowed.add(sha)
                pending.extend(self.parents(sha))
        events = []
        for sha in allowed:
            for event in json.loads(load_blob(self.packet,self.manifest['graphs'][sha]['events'])):
                if event['qn'] == symbol:
                    events.append({k:v for k,v in event.items() if k != 'qn'})
        return sorted(events,key=lambda e:e['position'])


def invoke(packet, manifest, name, args):
    if 'graphs' not in manifest:
        raise ValueError('No approved graph packet; curator export required')
    args = arguments(name, args)
    timeline = PacketTimeline(packet,manifest)
    timeline.authorize(args['commit'],manifest['task_sha'])
    store = Path('/work/graph-store')
    if name == 'graph_query':
        if str(packet) != '/packet' or not Path('/app/teacher/worker.py').exists():
            raise ValueError('Graph query requires the isolated runner')
        (store/'graphs').mkdir(parents=True,exist_ok=True)
        archive = load_blob(packet,manifest['graphs'][args['commit']]['backend'])
        (store/'graphs'/(args['commit']+'.db.gz')).write_bytes(archive)
    return GraphTools(timeline,manifest['task_sha'],store).invoke(name,args)
