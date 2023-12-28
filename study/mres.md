# Master's Thesis

![logo](./imperial.png ':size=40%')

In my MRes project, I concentrated on advancing **ovarian cancer diagnosis** through the application of **deep learning and image segmentation** techniques to ultrasound scans. The proposed model, developed with a focus on addressing the complexities presented by noisy ultrasound images and intricate tumor structures, incorporated vector quantisation, image segmentation, automatic quantitative and geometric analysis, and classification.

For the experimental setup, I conducted a thorough evaluation of the proposed model's performance using a dataset inclusive of ultrasound scans for ovarian cancer diagnosis. I analysed three distinct models: the **naive ResNet** (True Baseline), the **localised ResNet** (Advanced Baseline), and the **proposed pipeline**, which integrated vector quantisation, image segmentation, and a random forest classifier into one continuous pipeline. I meticulously examined key performance indicators for each model, considering the imbalanced class distribution of the dataset.

-   F1 score
-   accuracy
-   AUC-ROC
-   precision
-   recall

Comparisons were drawn with the Ovarian Diagnosis Score Radiomics Model (ODS), which is the current state-of-the-art.

## Proposed model architecture <!-- {docsify-ignore} -->

![logo](./mres-auto-seg-model.png ':size=WIDTHxHEIGHT')

The study's outcomes showcased the effectiveness of the proposed model in automating the segmentation process, leading to accelerated diagnostics with enhanced consistency and reduced human-induced errors. Notably, the model exhibited **resilience to segmentation inaccuracies**, thanks to its high-dimensional data representation and the **robustness of the random forest classifier**.

In the conclusion, I underscored the potential of integrating deep learning and image segmentation techniques for ovarian cancer diagnosis. The proposed model, with its automated segmentation, advanced data processing, and machine learning, exhibited promise for real-time diagnosis applications and broader contributions to medical imaging analysis.

The thesis outlined avenues for future work, including exploring challenges in multi-class segmentation with vector quantisation, addressing textural misclassification through prior medical knowledge incorporation, and investigating innovative methodologies for automated feature extraction and quantitative analysis. Emphasis was placed on the importance of external and extensive validation of the proposed model in real-world clinical settings.

In summary, my thesis contributed significantly to the field by presenting a model seamlessly integrating automatic segmentation into traditional diagnostic frameworks, showcasing its potential for enhancing ovarian cancer diagnosis.
