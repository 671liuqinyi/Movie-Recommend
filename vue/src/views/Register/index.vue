<template>
  <div>
    <Header></Header>
    <div class="login w">
      <div class="content">
        <div class="login-box">
          <h1 class="title">注册</h1>
          <div class="username">
            <span>用户名: </span>
            <input type="text" v-model="username" placeholder="请输入用户名">
          </div>
          <div class="password">
            <span>密码: </span>
            <input type="password" v-model="password" placeholder="请输入密码">
          </div>
          <div class="passwordconfirm">
            <span>确认密码: </span>
            <input type="password" v-model="confirm" placeholder="请再次输入密码">
          </div>
          <div class="foot">
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
      password: '',
      confirm: ''
    }
  },
  methods: {
    async register() {
      if (this.username == '' || this.password == '' || this.confirm == '') {
        this.$message.error('有必填项未填!')
        return
      }
      if (this.password != this.confirm) {
        this.$message.error(`两次输入密码不一致!`)
        this.confirm = ''
      } else {
        let result = await aixos.post('/api/register', {
          username: this.username,
          password: this.password
        })
        console.log(result.data)
        if (result.data.code == '200') {
          this.$message.success(`注册成功!`)
          this.$router.push('/login')
          this.username = ''
          this.password = ''
          this.confirm = ''
        } else {
          this.$message.error(`用户名已存在,注册失败!`)
          this.username = ''
        }
      }
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
  height: 320px;
  width: 500px;
  margin: 0 auto;
}
.login-box {
  float: left;
  margin-top: 120px;
  height: 320px;
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
.password,
.passwordconfirm {
  height: 40px;
  line-height: 40px;
  text-align: center;
  margin: 20px 0px;
  font-size: 20px;
}
.username,
.password {
  margin-left: 20px;
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
  width: 160px;
  height: 40px;
  text-align: center;
  line-height: 40px;
  background-color: #fff;
  text-decoration: none;
  border-radius: 5px;

  cursor: pointer;
}

.btn2 {
  float: left;
  margin-left: 180px;
}

.btn2:hover {
  background-color: #d2232a;
  color: #fff;
}
</style>