"""Offline reference for revision/grant checking. No LLM or design publication."""
import json

class Denied(Exception): pass

class Broker:
    def __init__(self, revision, grants):
        self.revision = revision
        self.grants = frozenset(grants)
        self.remaining = 8

    def call(self, request):
        # Real host must bound input BEFORE JSON parse, authenticate, check deadline,
        # isolate provider and persist audit log. This only demonstrates local policy.
        if not isinstance(request, dict) or set(request) != {'tool','revision','arguments'}:
            raise Denied('malformed envelope')
        if request['revision'] != self.revision:
            raise Denied('stale revision')
        if not isinstance(request['tool'], str) or not isinstance(request['arguments'],dict):
            raise Denied('malformed tool')
        if self.remaining <= 0:
            raise Denied('budget exhausted')
        tool, args = request['tool'],request['arguments']
        self.remaining -= 1
        if tool == 'design.get_revision' and 'design.read' in self.grants and not args:
            return {'revision':self.revision,'components':4,'provenance':'synthetic fixture'}
        if tool == 'analysis.explain_diagnostic' and 'design.read' in self.grants and args == {'id':'ERC-001'}:
            return {'revision':self.revision,'evidence':[{'id':'ERC-001','message':'Required power pin has no connection'}]}
        if tool == 'design.propose' and 'design.propose' in self.grants and set(args)=={'reason','candidate'}:
            if not isinstance(args['reason'],str) or not 1<=len(args['reason'])<=256 or not isinstance(args['candidate'],str) or not 1<=len(args['candidate'])<=4096:
                raise Denied('candidate limit/type')
            return {'revision':self.revision,'status':'UNVERIFIED_PROPOSAL','candidate':args['candidate'],'reason':args['reason']}
        raise Denied('tool, grant or arguments not admitted')

if __name__=='__main__':
    broker=Broker('fixture-r1',{'design.read','design.propose'})
    def call(tool,args,rev='fixture-r1'):return broker.call({'tool':tool,'revision':rev,'arguments':args})
    assert call('design.get_revision',{})['components']==4
    assert call('analysis.explain_diagnostic',{'id':'ERC-001'})['evidence'][0]['id']=='ERC-001'
    assert call('design.propose',{'reason':'review supply','candidate':'candidate text'})['status']=='UNVERIFIED_PROPOSAL'
    for tool,args,rev in [('design.apply',{},'fixture-r1'),('shell',{},'fixture-r1'),('instrument.set_output',{},'fixture-r1'),('design.get_revision',{},'fixture-r0')]:
        try:call(tool,args,rev)
        except Denied:pass
        else:raise AssertionError('unexpected grant')
    denied=Broker('fixture-r1',{'design.read'})
    try:denied.call({'tool':'design.propose','revision':'fixture-r1','arguments':{'reason':'x','candidate':'y'}})
    except Denied:pass
    else:raise AssertionError('unexpected proposal grant')
    print('PASS offline broker: revision, scope, read evidence, candidate only, denied publish/shell/instrument')
