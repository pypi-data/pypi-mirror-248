# 公众号消息回复服务

## 1. 项目介绍

本项目是一个基于 [Flask](https://flask.palletsprojects.com/en/1.1.x/) 的**微信公众号/订阅号的自动回复消息的简单服务框架
**。
使用者只需要实现两个简单的函数，即可快速搭建一个企业微信机器人回调功能的接口服务。

实现过程参考 [微信公众平台开发者文档-基础消息能力/接收普通消息](https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Receiving_standard_messages.html)
和 [被动回复用户消息](https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Passive_user_reply_message.html)
两个文档进行实现。

## 2. demo 效果

使用 demo/demo.py 中的示例，可以直接将实现一个 ECHO 功能的公众号服务。

## 3. 使用
