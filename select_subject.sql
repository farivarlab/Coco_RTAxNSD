--for azure sql

SELECT 
	[nsdId],
	[flagged] ,
	[BOLD5000],
	[shared1000],
	[subject1] ,
	[subject1_rep0],
	[subject1_rep1],
	[subject1_rep2]
 INTO
[dbo].[nsd_stim_info_subj1]
FROM nsd_stim_info
WHERE subject1 = 1
