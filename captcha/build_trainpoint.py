# -*- coding: utf-8 -*-
import sys,os,shutil,random,time
from captcha.image import ImageCaptcha

# 用于生成验证码的字符集
CHAR_SET = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
# 字符集的长度
CHAR_SET_LEN = 10
# 验证码的长度，每个验证码由4个数字组成
CAPTCHA_LEN = 4

# 验证码图片的存放路径
CAPTCHA_IMAGE_PATH = 'E:/captcha_img/images/'
# 用于模型测试的验证码图片的存放路径，它里面的验证码图片作为测试集
TEST_IMAGE_PATH = 'E:/captcha_img/test/'
# 用于模型测试的验证码图片的个数，从生成的验证码图片中取出来放入测试集中
TEST_IMAGE_NUMBER = 50


# 生成验证码图片，4位的十进制数字可以有10000种验证码
def generate_captcha_image(charSet=CHAR_SET, charSetLen=CHAR_SET_LEN, captchaImgPath=CAPTCHA_IMAGE_PATH):
    k = 0
    total = 1
    for i in range(CAPTCHA_LEN):
        total *= charSetLen

    for i in range(charSetLen):
        for j in range(charSetLen):
            for m in range(charSetLen):
                for n in range(charSetLen):
                    captcha_text = charSet[i] + charSet[j] + charSet[m] + charSet[n]
                    # 生成验证码
                    image = ImageCaptcha()
                    image.write(captcha_text, output=captchaImgPath+captcha_text + '.jpg')
                    k += 1
                    sys.stdout.write("\rCreating %d/%d" % (k, total))
                    # 刷新stdout，每隔一秒输出一个数字了
                    sys.stdout.flush()


# 从验证码的图片集中取出一部分作为测试集，这些图片不参加训练，只用于模型的测试
def prepare_test_set():
    fileNameList = []
    for filePath in os.listdir(CAPTCHA_IMAGE_PATH):
        captcha_name = filePath.split('/')[-1]
        fileNameList.append(captcha_name)
    random.seed(time.time())
    random.shuffle(fileNameList)
    for i in range(TEST_IMAGE_NUMBER):
        name = fileNameList[i]
        shutil.move(CAPTCHA_IMAGE_PATH + name, TEST_IMAGE_PATH + name)


if __name__ == '__main__':
    generate_captcha_image(CHAR_SET, CHAR_SET_LEN, CAPTCHA_IMAGE_PATH)
    prepare_test_set()
    sys.stdout.write("\nFinished")
    sys.stdout.flush()



























