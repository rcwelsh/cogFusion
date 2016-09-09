''' test the cogFusion_rcw'''

# to test this, do:
#
#    from test_rcw import *
#    test_all()
#
# this does require an original/ directory and the EPI_MASK_NOEYES.img/hdr pair.
#
# answer should be:
#
# ['original/3153.nii.gz', 'original/3154.nii.gz', 'original/3155.nii.gz']
# ['EPI_MASK_NOEYES.img']
# testing contrastDocProductAvg
# 1.0
# testing contrastAvgDocProduct
# [1.0000000000000002, 0.96397000438290426, 0.47014563818126826, 0.96397000438290426, 0.99999999999999989, 0.47736370554624213, 0.47014563818126831, 0.47736370554624213, 1.0]


from cogFusion_rcw import *

def test_all():

    
    nameList = ["original/3153.nii.gz", "original/3154.nii.gz","original/3155.nii.gz"]

    print(nameList)
    
    maskList = ["EPI_MASK_NOEYES.img"]

    print(maskList)
    
    testImageList = readImageList(nameList)
    
    maskImage = readImageList(maskList)
    
    ans1 = contrastDotProductAvg(testImageList,testImageList,maskImage)
    
    print("testing contrastDocProductAvg")
    
    print(ans1)

    print("testing contrastAvgDocProduct")

    ans2 = contrastAvgDotProduct(testImageList,testImageList,maskImage)

    print(ans2)
    

