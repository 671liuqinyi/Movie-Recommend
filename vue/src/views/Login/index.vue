<template>
  <div>
    <Header></Header>
    <div class="login w">
      <div class="content">
        <div class="login-box">
          <h1 class="title">登录</h1>
          <div class="username">
            <span>用户名: </span>
            <input type="text" v-model="username" placeholder="请输入用户名">
          </div>
          <div class="password">
            <span>密码: </span>
            <input type="password" v-model="password" placeholder="请输入密码">
          </div>
          <div class="foot">
            <a @click="login" class="btn1">登录</a>
            <a @click="register" class="btn2">注册</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import aixos from 'axios'
export default {
  name: '',
  data() {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    async login() {
      if(sessionStorage.getItem('username')){
        this.$message.error(`您已经处于登录状态!`)
        return 
      }
      // console.log(sessionStorage.getItem('username'))
      let result = await aixos.post('/api/login', {
        username: this.username,
        password: this.password
      })
      console.log(result.data)
      if (result.data.code == '200') {
        this.$message.success(`登录成功,欢迎${this.username}!`)
        sessionStorage.setItem('username', this.username)
        this.username = ''
        this.password = ''
        this.$router.push('/home')
      } else {
        this.$message.error(`登录失败,请检查用户名或密码是否正确!`)
        this.password = ''
      }
    },
    register() {
      this.$router.push('/register')
    }
  }
}
</script>
<style lang='less' scoped>
.login {
  height: 500px;
  background: url(./images/bg2.jpg);
}
.content {
  height: 300px;
  width: 500px;
  margin: 0 auto;
}
.login-box {
  float: left;
  margin-top: 120px;
  height: 300px;
  width: 500px;
  border: #ccc solid 1px;
  background-color: #ccc;
  border-radius: 10px;
}
.title {
  margin-top: 20px;
  height: 40px;
  text-align: center;
  // line-height: 40px;
  width: 100%;
  font-weight: normal;
  // border: 1px solid #ccc;
}
.username,
.password {
  height: 40px;
  line-height: 40px;
  text-align: center;
  margin: 20px 0px;
  font-size: 20px;
}
input {
  height: 20px;
  padding-left: 10px;
  outline: medium;
}
.password input {
  margin-left: 20px;
}
a {
  display: block;
  width: 80px;
  height: 40px;
  text-align: center;
  line-height: 40px;
  background-color: #fff;
  text-decoration: none;
  border-radius: 5px;

  cursor: pointer;
}
.btn1 {
  float: left;
  margin-left: 160px;
}

.btn2 {
  float: right;
  margin-right: 120px;
}
.btn1:hover,
.btn2:hover {
  background-color: #d2232a;
  color: #fff;
}
</style>