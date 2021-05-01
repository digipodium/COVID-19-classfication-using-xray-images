## COVID-19 classfication
### Automated Detection of COVID-19 Cases Using Deep Neural Networks with X-Ray Images

In this study, a deep learning model is proposed for the automatic diagnosis of COVID-19. The proposed model is developed to provide accurate diagnostics for multi-class classification (COVID vs. No-Findings vs. Pneumonia). Our model produced an average classification accuracy of 87.02% for multi-class cases when train for 100 iteration. 

[X-ray images](#) obtained from two different sources were used for the diagnosis of COVID-19. A COVID-19 X-ray image [database](https://github.com/ieee8023/COVID-chestxray-dataset/)  was developed by Cohen JP using images from various open access sources. This database is constantly updated with images shared by researchers from different regions. 

Also, the [ChestX-ray8 database](http://openaccess.thecvf.com/content_cvpr_2017/papers/Wang_ChestX-ray8_Hospital-Scale_Chest_CVPR_2017_paper.pdf) provided by Wang et al. was used for normal and pneumonia images. In order to avoid the unbalanced data problem, we used 500 no-findings and 500 pneumonia class frontal chest X-ray images randomly from this database. 
