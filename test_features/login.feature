@login
Feature: 登录模块
    需求描述: 用户进入登录页面/弹窗登录页面，使用正确用户名以及密码可以登录成功
    @todo
    Scenario: 弹窗登录: 正确用户名和密码登录成功
        Given 打开浏览器，访问项目首页<host>/explore
        When 点击导航栏右上角的登录按钮，打开登录弹窗
        And 弹窗中，我输入以下信息进行登录：
            | 用户名    | 密码       |
            | auotest  | 12345678  |
        And 弹窗中，点击: 登录按钮， 提交登录表单
        Then 登录成功，当前页面的url地址应该是：<host>/explore
        And 登录成功，导航栏右上角显示的用户昵称应该是：auotest

    @todo
    Scenario: 网页登录: 正确用户名和密码登录成功
        Given 打开浏览器，访问GitLink首页<host>
        When 点击导航栏右上角的登录按钮，进入登录页面
        And 登录页面中，我输入以下信息进行登录：
            | 用户名    | 密码       |
            | auotest  | 12345678  |
        And 登录页面中，点击: 登录按钮， 提交登录表单
        Then 登录成功，当前页面的url地址应该是：<host>/auotest
        And 登录成功，导航栏右上角显示的用户昵称应该是：auotest
    @todo
    Scenario Outline: 网页登录: 用户名正确，密码错误，有密码错误次数提示
        Given 打开浏览器，访问GitLink首页<host>
        When 点击导航栏右上角的登录按钮，进入登录页面
        And 登录页面中，我输入以下信息进行登录：
            | 用户名    | 密码         |
            | <login>  | <password>  |
        And 登录页面中，点击: 登录按钮， 提交登录表单
        Then 登录失败，页面有密码错误提示：<expected_error>
        Examples:
          |  host    | login          |    password     |   expected_error                                         |
          |  <host>  | floratest1     |    12345111     |   你已经输错密码1次，还剩余4次机会                             |
          |  <host>  | floratest1     |    123456xxx    |   你已经输错密码2次，还剩余3次机会                             |
          |  <host>  | floratest1     |    123456xxx    |   你已经输错密码3次，还剩余2次机会                             |
          |  <host>  | floratest1     |    123456xxx    |   你已经输错密码4次，还剩余1次机会                             |
          |  <host>  | floratest1     |    123456xxx    |   登录密码出错已达上限，账号已被锁定, 请60分钟后重新登录或找回密码   |
