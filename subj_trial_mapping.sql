--for Azure sql
if not exists (select * from sys.TABLES WHERE name = 'subj1_trial_mapping')
BEGIN
    create table subj1_trial_mapping(
        trialID INT PRIMARY KEY,
        nsdID INT NOT NULL
    );
end;

INSERT INTO subj1_trial_mapping (trialID, nsdId)
SELECT subject1_rep0, nsdId FROM nsd_stim_info_subj1 WHERE subject1_rep0 > 0
UNION ALL
SELECT subject1_rep1, nsdId FROM nsd_stim_info_subj1 WHERE subject1_rep1 > 0
UNION ALL
SELECT subject1_rep2, nsdId FROM nsd_stim_info_subj1 WHERE subject1_rep2 > 0;