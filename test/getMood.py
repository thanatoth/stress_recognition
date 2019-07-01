import numpy as np

# feature[0:8]
# 0:HAPPY, 1:SAD, 2:ANGRY, 3:CONFUSED, 4:DISGUSTED, 5:SURPRISED, 6:CALM, 7:SMILE, 8:照度, 9:心拍数
def getMood(feature) :
    # 係数の設定
    coef = np.array([1, -1, -1, -0.5, -0.5, -0.25, 1, 0.2, 0.2, 0.2], dtype="float64")
    illum_ref = 650.0
    heart_ref = 70.0

    # 特徴量の正規化
    feature[0:6] /= 100.0

    # 照度の変換
    feature[8] -= illum_ref
    feature[8] = transGauss(feature[8], 0.0, 10000.0)

    # 心拍数の変換
    feature[9] -= heart_ref
    feature[9] = transGauss(feature[9], 0.0, 100.0)

    score = sum(coef * feature)

    #return classifyMood(score)

    print(score)
    print(classifyMood(score))

# キゲン分類
def classifyMood(score):
    if score > 0.5: # キゲンが良い
        return 0
    elif score < -0.5: # キゲンが悪い
        return 2
    else : # キゲンが普通
        return 1

# ガウス変換
def transGauss(data, mu, sigma2):
    data = GaussDist(data, mu, sigma2)
    data /= GaussDist(0.0, mu, sigma2) # 最大値で正規化 -> 0-1 のレンジ
    data -= 0.5 # -> -0.5 - 0.5 のレンジ
    data *= 2.0 # -> -1.0 - 1.0 のレンジ

    return data

# ガウス分布関数
def GaussDist(X, mu, sigma2):
    return 1.0/np.power(2.0*np.pi*sigma2,1/2) * np.exp(-1*np.power(X-mu,2)/(2*sigma2))


if __name__ == '__main__':
    # feature[0:8]
    # 0:HAPPY, 1:SAD, 2:ANGRY, 3:CONFUSED, 4:DISGUSTED, 5:SURPRISED, 6:CALM, 7:SMILE, 8:照度, 9:心拍数
    test_feature = np.array([70,20,0,3,2,1,0,1,512,110], dtype="float64")

    getMood(test_feature)