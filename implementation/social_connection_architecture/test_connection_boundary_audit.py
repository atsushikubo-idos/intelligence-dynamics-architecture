"""Unittest audit of mathematical claims and negative conditions."""
import unittest
from connection_boundary_audit import *

class BoundaryTests(unittest.TestCase):
    def setUp(self):
        self.actions=('left','right'); self.actors=('A','B')
        self.worlds=(make_world('0',('?',),{'A':{'left'},'B':{'left'}}),
                     make_world('1',('?',),{'A':{'right'},'B':{'right'}}))

    def test_indistinguishable_conflicting_worlds_no_robust_action(self):
        r=boundary(self.worlds,'decision',self.actors,('?',),self.actions)
        self.assertEqual(r.status,'POSSIBLE_NOT_GUARANTEED')
        self.assertEqual(r.guaranteed_actions,())
    def test_disjoint_witness(self):
        self.assertEqual(observational_impossibility_witness(self.worlds,'decision',self.actors,('?',),self.actions),('0','1'))
    def test_observation_refines_possible_worlds(self):
        worlds=(make_world('0',('left',),{'A':{'left'},'B':{'left'}}),
                make_world('1',('right',),{'A':{'right'},'B':{'right'}}))
        r=boundary(worlds,'decision',self.actors,('left',),self.actions)
        self.assertEqual(r.guaranteed_actions,('left',))
    def test_full_internal_knowledge_not_required(self):
        worlds=(make_world('private-state-0',('shared',),{'A':{'left'},'B':{'left'}}),
                make_world('private-state-1',('shared',),{'A':{'left'},'B':{'left'}}))
        self.assertEqual(boundary(worlds,'decision',self.actors,('shared',),self.actions).status,'GUARANTEED')
    def test_no_joint_action_any_world(self):
        w=make_world('0',('?',),{'A':{'left'},'B':{'right'}})
        self.assertEqual(boundary((w,),'decision',self.actors,('?',),self.actions).status,'IMPOSSIBLE')
    def test_refusal_separate_from_unobservability(self):
        w=make_world('0',('fully-known',),{'A':{'left'},'B':set()})
        self.assertEqual(boundary((w,),'decision',self.actors,('fully-known',),self.actions).status,'IMPOSSIBLE')
    def test_three_states_domains(self):
        w=World('w',('known',),{'shared':{'A':frozenset({'left'}),'B':frozenset({'left'})},
                               'private':{'A':frozenset({'right'}),'B':frozenset({'left'})}})
        state,out=classify_domains((w,),('shared','private'),self.actors,('known',),self.actions)
        self.assertEqual(state,'LIMITED')
        self.assertEqual(out['private'].status,'IMPOSSIBLE')
    def test_three_state_connected(self):
        w=World('w',('known',),{'a':{'A':frozenset({'left'}),'B':frozenset({'left'})},
                                'b':{'A':frozenset({'left'}),'B':frozenset({'left'})}})
        self.assertEqual(classify_domains((w,),('a','b'),self.actors,('known',),self.actions)[0],'CONNECTED')
    def test_three_state_disconnected(self):
        w=World('w',('known',),{'a':{'A':frozenset({'left'}),'B':frozenset({'right'})},
                                'b':{'A':frozenset({'right'}),'B':frozenset({'left'})}})
        self.assertEqual(classify_domains((w,),('a','b'),self.actors,('known',),self.actions)[0],'DISCONNECTED')
    def test_temporal_refusal_reconnection(self):
        self.assertEqual([r.status for _,r in temporal_example()],
                         ['POSSIBLE_NOT_GUARANTEED','GUARANTEED','IMPOSSIBLE','GUARANTEED'])
    def test_pairwise_cannot_identify_joint(self):
        r=triadic_counterexample()
        self.assertTrue(r['pairwise_marginals_equal'])
        self.assertTrue(r['full_joint_distinguishes'])
        self.assertEqual(r['xor_even_parity_rate'],1.0)
        self.assertEqual(r['independent_even_parity_rate'],0.5)
    def test_third_actor_can_block_and_unblock(self):
        self.assertEqual(two_vs_three_example(),{
            'two':'GUARANTEED','three_with_conflict':'IMPOSSIBLE','three_with_permission':'GUARANTEED'})
    def test_absence_of_pairwise_witness_does_not_imply_global_common_action(self):
        # {a,b}, {b,c}, {a,c}: pairwise intersections all nonempty, global empty.
        actions=('a','b','c')
        worlds=tuple(make_world(str(k),('?',),{'A':s,'B':s}) for k,s in enumerate(({'a','b'},{'b','c'},{'a','c'})))
        self.assertIsNone(observational_impossibility_witness(worlds,'decision',self.actors,('?',),actions))
        self.assertEqual(boundary(worlds,'decision',self.actors,('?',),actions).status,'POSSIBLE_NOT_GUARANTEED')
    def test_inconsistent_evidence_raises(self):
        with self.assertRaises(ValueError): boundary(self.worlds,'decision',self.actors,('nonexistent',),self.actions)
    def test_empty_actions_raise(self):
        with self.assertRaises(ValueError): boundary(self.worlds,'decision',self.actors,('?',),())

if __name__=='__main__': unittest.main()
