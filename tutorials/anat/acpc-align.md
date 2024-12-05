---
title: "Align AC PC to horizontal"
description: "Translate your structural scans to AC-PC alignment for visualization and display."
author: "Danny Kim"
date: "2024/12/04"
date-modified: "2024/12/04"
highlight-style: github
categories:
    - anat
    - shell
    - code
    - visualization
    - alignment
---

# Align to the Anterior Commissure-Posterior Commisure Line

If you need help determining where the Anterior and Posterior Commisures are in your image, please see [Commissural Pathways](https://www.kenhub.com/en/library/anatomy/commissural-pathways), available online,  or [Catani & Thiebaut de Schotten (2012)](https://academic.oup.com/book/24732/chapter-abstract/188237007?redirectedFrom=fulltext), which is available from the UBC Library.

1. Download the [`acpc_align`](./acpc_align.sh) script from [here](./acpc_align.sh). Be sure the code is in the folder where your participant's structural scans are.

2. Make the acpc_align.sh script executable.
```{.shell}
chmod 755 acpc_align.sh
```

2. Open your structural scan in your faviourite viewer. Here we are using FSLeyes.

![FSLeyes](images/base_fsleyes.png)

3. Get the X, Y and Z coordinates of the anterior commissure in voxel space by placing your cursor on the anterior commissure. The anterior commissure is located in the anterior wall of the third ventricle. It runs transversely anterior to the anterior columns of the fornix, above the basal forebrain and beneath the medial and ventral aspect of the anterior limb of the internal capsule. Save the X, Y, and Z coordinates.

![Anterior Commissure](images/anteriorcommissure.png)

4. Get the X, Y, and Z coordinates of the posterior commissure in voxel space by placing your cursor on the posterior commissure. The posterior commissure is the inferior lamina or stalk of the pineal gland. Save the X, Y, and Z coordinates.

![Posterior Commissure](images/posteriorcommissure.png)

5. In your terminal (MacOS or Linux) run
```{.shell}
acpc_align subjectbrain.nii.gz -a x y z -p x y z
```
to produce the realigned image for subject-specific to acpc alignment.


In the example, this is
```{.shell}
sh acpc_align.sh T1_reoriented.nii.gz -a 93 130 153 -p 93 98 152
```

![acpc aligned image](./images/acpc_aligned.png)


