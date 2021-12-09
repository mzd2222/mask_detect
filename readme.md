## 1 登录 注册 登出

1. 功能: 注册
   方法: POST
   地址: /login_register/register/
   提交数据示例：JSON

   ```json
   {
       "username": "mzd",
       "password": "123456",
       "email": "256598@qq.com",
       "authority": true,  //or false 是否为管理员账号
   }
   ```
   返回值: JSON
   ```json
   {
       "state": "ok",    //ok或error标示注册是否成功 
       "msg": ""         //成功返回空 失败返回错误信息
       // msg_error:传入信息错误；method_error:错误的请求方式；
   }
   ```  


2. ```json
   //功能：登录
   //方法：POST
   //地址：/login_register/login/
   //提交数据示例：JSON:
   {
       "username": "mzd",
       "password": "123456"
   }
   //返回值：JSON 
   {
        "state"： "ok",  //ok或error标示登录是否成功,
        "msg"：  ""     //成功返回用户对象（待定） 失败返回错误信息
   }
   //错误信息：login_error:账号或密码错误；method_error_repeat_login_error:重复登录或错误请求方式;
   //返回示例 JSON 
   {
       "state": "error",
       "msg": "method_error_repeat_login_error"
   }
   
3. ```
   功能：登出当前账户
   方法：GET
   地址：/login_register/logout/
   数据示例：无
   返回：
       成功返回：{"state": "ok", "msg":""}
       错误返回：{"state": "error", "msg": "method_error repeat_logout"}

## 2 用户反馈



## 3 资源相关

1. ```json
   功能：获取登录的用户剩余资源（需要登录）
   方法：GET
   地址：/mask_detect/get_user_resources/
   数据示例：无
   返回：
   	正确返回：
        {
           "state": "ok",
           "resources":
              {
           	"resource_table_id": 1,
           	"user_id": 8,
           	"img_nums": 100,     //剩余可处理图片数量
           	"camera_nums": 100,  //剩余可部署摄像头数量
           	"video_nums": 100    //剩余可处理视频数量
               }
         }
   	错误返回：{"state": "error"}
   ```

2. ```json
   功能：获取用户已购买的摄像头 或 未占用的摄像头
   方法：GET
   地址：/mask_detect/get_user_resources/?state=0
   数据说明：state=0 表示获取未使用的相机
           state=1 表示获取当前用户已购买的相机
   返回：
     正确返回：
        {
           "state": "ok",
           "cameras": []
         }
     其中cameras值为一个序列化后的对象数组，每个数组元素代表一个摄像头：
        {
            "camera_id": 1,        // 在绑定用户和摄像头时需要使用camera_id,需要保存下来
            "camera_name": "123",  // 摄像头名称
            "user_id": null,       // 已绑定的用户id，未绑定则为空
            "desc": "good camera"  // 摄像头描述
        }
   
     错误返回：{"state": "error"} 方法错误
   ```

   

3. ```json
   功能：用户绑定摄像头（即摄像头与用户绑定）
   方法：POST
   要求：需要登录以及POST方法
   地址：/mask_detect/user_add_camera/
   提交数据示例：{"camera_id": 1} camera_id为接口3.3中获取到的未使用的camera_id
   返回：
   	错误返回：
               {"state": "error"} 未登录或方法错误
   			{"state": "no resources"}  用户资源不够，需要购买后再添加
   	正确返回：
               {"state": "ok"}
   ```

4. ```json
   功能：创建新摄像头
   方法：POST
   要求：需要管理员登录以及POST方法
   地址：/mask_detect/create_camera/
   提交数据示例：{"name": "good", "description": "very good camera"} 
               name为摄像头名，discription为摄像头描述
   返回：
   	正确返回：
               {"state": "ok"}
   	错误返回：
               {"state": "error"} 
   ```

5. ```json
   功能：增加用户资源resources
   方法：POST
   要求：需要登录以及POST方法
   地址：/mask_detect/add_user_resources/
   提交数据示例：{"state_code": "0", "number": "10"} 
   			state_code="0"：增加图片数量
   			state_code="1"：增加摄像头数量
   			state_code="2"：增加视频数量
               number为增加的数量,增加到当前登录用户
   返回：
   	正确返回：
               {"state": "ok"}
   	错误返回：
               {"state": "error"} 未登录或方法错误
   ```

6. ```json
   功能：用户上传处理图片
   方法：POST
   要求：需要登录以及POST方法
   地址：/mask_detect/picture_calculate/
   提交数据示例：{"pic_file": "图片文件"} 需要以POST方式直接上传图片文件
   返回：
   	错误返回：
               {"state": "error1"} 未登录或方法错误
               {"state": "error2"} 未提交文件或提交文件错误
   			{"state": "no resources"}  用户资源不够，需要购买后再添加
   	正确返回：
               返回HttpResponse，填入图片src值即可显示 （TODO:待测试）
   ```

7. ```json
   功能：用户上传处理视频
   方法：POST
   要求：需要登录以及POST方法
   地址：/mask_detect/video_calculate/
   提交数据示例：{"video_file": "视频文件"} 需要以POST方式直接上传视频文件
   返回：
   	错误返回：
               {"state": "error1"} 未登录或方法错误
               {"state": "error2"} 未提交文件或提交文件错误
   			{"state": "no resources"}  用户资源不够，需要购买后再添加
   	正确返回：
               {"state": "ok", "url": "download_path"}
   			download_path为视频下载连接，get这个连接即能下载处理好的视频
   ```

8. 

