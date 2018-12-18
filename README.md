# Spider爬虫实例

## 1. dianping——大众点评
* 大众点评获取所有排行榜店铺信息建表入库
* selenium登录获取cookie，使用cookie模拟登录
* 从库中获取所有店铺的id，拼接URL获取每个店铺所有评论信息并建表入库
* 添加断点续爬功能，程序中断后自动从断点开始爬取。

## 2. zhihuCrawl——知乎web
* 知乎模拟登录
* 验证码图片保存，输入识别的验证码
* 获取当日热门话题及其高赞回答
* 保存问题标题、链接，回答者的ID，内容及点赞数量，存储至MongoDB

## 3. 微信公众号爬虫
* 使用西刺代理构建代理ip池，检查代理ip连通性
* 使用可用的ip爬取搜狗微信公众号文章
* 将文章保存为.doc文档

## 4. 豆瓣读书爬虫 	
* 读取豆瓣每个分类的书籍列表
* 获取每本书信息,存储到MySQL，爬取完毕后删除重复数据并重新排序

## 5. csdn_scrapy——csdn网站
* 爬取csdn所有子标签文章，清洗后保存到MongoDB 
* 使用scrapy.redis组件进行分布式部署

## 6. bilibili——b站 	
* 使用scrapy-splash爬取b站子标签热门video排行的大量信息
* 按标签建表保存至MongoDB 		

## 7. toutiao——今日头条web	
* 爬取今日头条子标签新闻
* webdriver获取加密参数
* ajax请求返回json数据解析，保存至MongoDB

## 8. taobao——淘宝web
* 爬取淘宝各子标签，按销量排名商品信息，按分类保存至MongoDB
* 通过pandas进行数据分析
* 将商品在各省分布、销量排行、地图分布等通过matplotlib绘图显示

## 9. zhihu_app——知乎app
* 爬取使用ssl-pinning技术的app
* fiddler抓包获取api请求
* 模拟手机端请求数据，解析json存入mysql

## 10. Ajax_weibo——微博app	
* 输入要爬取的博主ID，获取ajax请求
* 解析json数据，爬取博主所有微博，保存至MySQL 	

## 11. scrapyd 	
docker scrapyd 配置文件 	
