# Test result summary (generated)

| suite | implementation | total | pass | fail | error | xfail | unexpected_success | skip |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| phase2 | original | 37 | 17 | 15 | 0 | 5 | 0 | 0 |
| phase2 | proposed | 37 | 32 | 0 | 0 | 5 | 0 | 0 |
| phase2 | research_safe | 37 | 31 | 1 | 0 | 3 | 2 | 0 |
| integrity | original | 43 | 6 | 36 | 1 | 0 | 0 | 0 |
| integrity | proposed | 43 | 5 | 34 | 4 | 0 | 0 | 0 |
| integrity | research_safe | 43 | 43 | 0 | 0 | 0 | 0 | 0 |

## Per-test outcome differences between implementations

### phase2: original -> proposed (15 differences)

- `CycleEventOrder.test_demo_reports_event_order_not_cycle_completion`: fail -> pass
- `CycleEventOrder.test_event_order_true_does_not_imply_theoretical_cycle`: fail -> pass
- `CycleEventOrder.test_no_reopening_is_not_satisfied`: fail -> pass
- `CycleEventOrder.test_reopen_without_any_recontact_is_not_event_order_complete`: fail -> pass
- `CycleEventOrder.test_stale_contact_before_update_does_not_count`: fail -> pass
- `CycleEventOrder.test_update_then_recontact_then_reopen_satisfies_event_order`: fail -> pass
- `EvidenceChecks.test_reopening_provenance_states_semantic_adequacy_not_assessed`: fail -> pass
- `EvidenceChecks.test_unknown_evidence_id_is_rejected`: fail -> pass
- `FutureUpdateabilityConsistency.test_increased_without_recontact_route_is_rejected`: fail -> pass
- `HoldingResolution.test_ignored_unregistered_ids_are_recorded_in_provenance`: fail -> pass
- `HoldingResolution.test_partial_resolution_keeps_holding_active`: fail -> pass
- `HoldingResolution.test_partial_resolution_visible_in_cdp_description`: fail -> pass
- `HoldingResolution.test_unregistered_residual_id_is_not_counted_as_resolved`: fail -> pass
- `TrajectoryTransitions.test_reemergence_phase_requires_predecessor`: fail -> pass
- `TrajectoryTransitions.test_transition_cannot_revive_dissolved_trajectory`: fail -> pass

### phase2: original -> research_safe (16 differences)

- `CycleEventOrder.test_demo_reports_event_order_not_cycle_completion`: fail -> pass
- `CycleEventOrder.test_event_order_true_does_not_imply_theoretical_cycle`: fail -> pass
- `CycleEventOrder.test_no_reopening_is_not_satisfied`: fail -> pass
- `CycleEventOrder.test_reopen_without_any_recontact_is_not_event_order_complete`: fail -> pass
- `CycleEventOrder.test_stale_contact_before_update_does_not_count`: fail -> pass
- `CycleEventOrder.test_update_then_recontact_then_reopen_satisfies_event_order`: fail -> pass
- `EvidenceChecks.test_reopening_provenance_states_semantic_adequacy_not_assessed`: fail -> pass
- `EvidenceChecks.test_unknown_evidence_id_is_rejected`: fail -> pass
- `HoldingResolution.test_ignored_unregistered_ids_are_recorded_in_provenance`: fail -> pass
- `HoldingResolution.test_partial_resolution_keeps_holding_active`: fail -> pass
- `HoldingResolution.test_partial_resolution_visible_in_cdp_description`: fail -> pass
- `HoldingResolution.test_unregistered_residual_id_is_not_counted_as_resolved`: fail -> pass
- `OpenSpecDecisions.test_SPEC1_declared_L1_with_frame_replacement_is_rejected_or_flagged`: xfail -> unexpected_success
- `OpenSpecDecisions.test_SPEC3_compare_does_not_subtract_residual_counts_across_different_frames`: xfail -> unexpected_success
- `TrajectoryTransitions.test_reemergence_phase_requires_predecessor`: fail -> pass
- `TrajectoryTransitions.test_transition_cannot_revive_dissolved_trajectory`: fail -> pass

### phase2: proposed -> research_safe (3 differences)

- `FutureUpdateabilityConsistency.test_increased_without_recontact_route_is_rejected`: pass -> fail
- `OpenSpecDecisions.test_SPEC1_declared_L1_with_frame_replacement_is_rejected_or_flagged`: xfail -> unexpected_success
- `OpenSpecDecisions.test_SPEC3_compare_does_not_subtract_residual_counts_across_different_frames`: xfail -> unexpected_success

### integrity: original -> proposed (3 differences)

- `FUJudgmentRecord.test_increased_without_route_carries_non_binding_review_flag`: fail -> error
- `FUJudgmentRecord.test_increased_without_route_is_accepted_not_rejected`: pass -> error
- `FUJudgmentRecord.test_reopen_accepts_increased_without_route_and_records_judgment_nature`: fail -> error

### integrity: original -> research_safe (37 differences)

- `FUJudgmentRecord.test_cdp_description_exposes_judgment_nature_of_latest_fu`: fail -> pass
- `FUJudgmentRecord.test_demo_marks_fu_as_judgment_and_not_estimable`: fail -> pass
- `FUJudgmentRecord.test_increased_with_route_has_no_flag`: fail -> pass
- `FUJudgmentRecord.test_increased_without_route_carries_non_binding_review_flag`: fail -> pass
- `FUJudgmentRecord.test_measurement_status_latent_not_validated_with_perturbation_claim`: fail -> pass
- `FUJudgmentRecord.test_measurement_status_never_asserts_an_estimate`: fail -> pass
- `FUJudgmentRecord.test_measurement_status_not_estimable_without_perturbation_claim`: fail -> pass
- `FUJudgmentRecord.test_record_type_is_evaluator_judgment`: fail -> pass
- `FUJudgmentRecord.test_reduced_with_route_is_accepted_and_unflagged`: fail -> pass
- `FUJudgmentRecord.test_reopen_accepts_increased_without_route_and_records_judgment_nature`: fail -> pass
- `FUJudgmentRecord.test_route_presence_alone_neither_confirms_nor_denies`: error -> pass
- `FrameComparisonGate.test_blank_shared_measure_is_treated_as_absent`: fail -> pass
- `FrameComparisonGate.test_declared_shared_measure_returns_values_marked_unverified`: fail -> pass
- `FrameComparisonGate.test_different_frame_names_also_not_established`: fail -> pass
- `FrameComparisonGate.test_measurement_version_difference_not_returned_without_shared_measure`: fail -> pass
- `FrameComparisonGate.test_no_declared_measure_marks_not_established`: fail -> pass
- `FrameComparisonGate.test_residual_difference_not_returned_without_shared_measure`: fail -> pass
- `FrameComparisonGate.test_same_frame_name_does_not_establish_comparability`: fail -> pass
- `GapGuards.test_L5_with_frame_replacement_only_is_flagged`: fail -> pass
- `GapGuards.test_blank_or_non_string_perturbation_claims_stay_not_estimable`: fail -> pass
- `GapGuards.test_caller_cannot_inject_derived_fu_fields`: fail -> pass
- `GapGuards.test_compare_output_has_no_numeric_values_without_shared_measure`: fail -> pass
- `GapGuards.test_one_non_blank_claim_among_blanks_is_enough_for_latent_not_validated`: fail -> pass
- `GapGuards.test_translate_carries_fu_judgment_nature`: fail -> pass
- `UpdateLevelConsistency.test_L1_with_frame_replacement_is_flagged_as_definition_conflict`: fail -> pass
- `UpdateLevelConsistency.test_L1_with_no_change_has_no_flags`: fail -> pass
- `UpdateLevelConsistency.test_L2_with_frame_replacement_is_flagged_as_definition_conflict`: fail -> pass
- `UpdateLevelConsistency.test_L3_with_frame_and_space_gets_only_convention_dependent_flag`: fail -> pass
- `UpdateLevelConsistency.test_L3_with_frame_replacement_only_has_no_flags`: fail -> pass
- `UpdateLevelConsistency.test_L3_without_frame_replacement_is_flagged`: fail -> pass
- `UpdateLevelConsistency.test_L4_is_not_checked_for_frame_replacement`: fail -> pass
- `UpdateLevelConsistency.test_L5_with_space_replacement_has_no_flags`: fail -> pass
- `UpdateLevelConsistency.test_L5_without_space_replacement_is_flagged`: fail -> pass
- `UpdateLevelConsistency.test_boundary_or_measurement_change_alone_is_not_mapped_to_levels`: fail -> pass
- `UpdateLevelConsistency.test_demo_update_with_space_change_under_L3_carries_convention_flag`: fail -> pass
- `UpdateLevelConsistency.test_flags_are_also_recorded_in_provenance`: fail -> pass
- `UpdateLevelConsistency.test_module_level_checker_is_available_and_consistent`: fail -> pass

### integrity: proposed -> research_safe (38 differences)

- `FUJudgmentRecord.test_cdp_description_exposes_judgment_nature_of_latest_fu`: fail -> pass
- `FUJudgmentRecord.test_demo_marks_fu_as_judgment_and_not_estimable`: fail -> pass
- `FUJudgmentRecord.test_increased_with_route_has_no_flag`: fail -> pass
- `FUJudgmentRecord.test_increased_without_route_carries_non_binding_review_flag`: error -> pass
- `FUJudgmentRecord.test_increased_without_route_is_accepted_not_rejected`: error -> pass
- `FUJudgmentRecord.test_measurement_status_latent_not_validated_with_perturbation_claim`: fail -> pass
- `FUJudgmentRecord.test_measurement_status_never_asserts_an_estimate`: fail -> pass
- `FUJudgmentRecord.test_measurement_status_not_estimable_without_perturbation_claim`: fail -> pass
- `FUJudgmentRecord.test_record_type_is_evaluator_judgment`: fail -> pass
- `FUJudgmentRecord.test_reduced_with_route_is_accepted_and_unflagged`: fail -> pass
- `FUJudgmentRecord.test_reopen_accepts_increased_without_route_and_records_judgment_nature`: error -> pass
- `FUJudgmentRecord.test_route_presence_alone_neither_confirms_nor_denies`: error -> pass
- `FrameComparisonGate.test_blank_shared_measure_is_treated_as_absent`: fail -> pass
- `FrameComparisonGate.test_declared_shared_measure_returns_values_marked_unverified`: fail -> pass
- `FrameComparisonGate.test_different_frame_names_also_not_established`: fail -> pass
- `FrameComparisonGate.test_measurement_version_difference_not_returned_without_shared_measure`: fail -> pass
- `FrameComparisonGate.test_no_declared_measure_marks_not_established`: fail -> pass
- `FrameComparisonGate.test_residual_difference_not_returned_without_shared_measure`: fail -> pass
- `FrameComparisonGate.test_same_frame_name_does_not_establish_comparability`: fail -> pass
- `GapGuards.test_L5_with_frame_replacement_only_is_flagged`: fail -> pass
- `GapGuards.test_blank_or_non_string_perturbation_claims_stay_not_estimable`: fail -> pass
- `GapGuards.test_caller_cannot_inject_derived_fu_fields`: fail -> pass
- `GapGuards.test_compare_output_has_no_numeric_values_without_shared_measure`: fail -> pass
- `GapGuards.test_one_non_blank_claim_among_blanks_is_enough_for_latent_not_validated`: fail -> pass
- `GapGuards.test_translate_carries_fu_judgment_nature`: fail -> pass
- `UpdateLevelConsistency.test_L1_with_frame_replacement_is_flagged_as_definition_conflict`: fail -> pass
- `UpdateLevelConsistency.test_L1_with_no_change_has_no_flags`: fail -> pass
- `UpdateLevelConsistency.test_L2_with_frame_replacement_is_flagged_as_definition_conflict`: fail -> pass
- `UpdateLevelConsistency.test_L3_with_frame_and_space_gets_only_convention_dependent_flag`: fail -> pass
- `UpdateLevelConsistency.test_L3_with_frame_replacement_only_has_no_flags`: fail -> pass
- `UpdateLevelConsistency.test_L3_without_frame_replacement_is_flagged`: fail -> pass
- `UpdateLevelConsistency.test_L4_is_not_checked_for_frame_replacement`: fail -> pass
- `UpdateLevelConsistency.test_L5_with_space_replacement_has_no_flags`: fail -> pass
- `UpdateLevelConsistency.test_L5_without_space_replacement_is_flagged`: fail -> pass
- `UpdateLevelConsistency.test_boundary_or_measurement_change_alone_is_not_mapped_to_levels`: fail -> pass
- `UpdateLevelConsistency.test_demo_update_with_space_change_under_L3_carries_convention_flag`: fail -> pass
- `UpdateLevelConsistency.test_flags_are_also_recorded_in_provenance`: fail -> pass
- `UpdateLevelConsistency.test_module_level_checker_is_available_and_consistent`: fail -> pass

