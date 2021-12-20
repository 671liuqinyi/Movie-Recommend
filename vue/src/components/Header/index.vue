<template>
  <div class="header w">
    <div class="logo" @click="returnHome">
      <img src="./images/logo.png" alt="">
    </div>
    <div class="nav">
      <ul>
        <li><a href="/recommend?type=plot">剧情</a></li>
        <li><a href="/recommend?type=horror">恐怖</a></li>
        <li><a href="/recommend?type=comedy">喜剧</a></li>
        <li><a href="/recommend?type=suspense">悬疑</a></li>
        <li><a href="/recommend?type=love">爱情</a></li>
        <li><a @click="personalrecommend" class="personalrecommend">个性推荐</a></li>
      </ul>
    </div>
    <div class="search">
      <input type="text" placeholder="请输入电影名称" v-model="input">
      <button @click="search"></button>
    </div>
    <div class="nav rightnav">
      <ul>
        <li><a @click="chooseinterests">兴趣选择</a></li>
        <li v-if="state"><a href="/login">登录</a></li>
        <li v-else>
          <a>
            <el-dropdown @command="handleCommand">
              <span class="el-dropdown-link">
                {{nickname==''?'用户':nickname}}<i class="el-icon-arrow-down el-icon--right"></i>
              </span>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item command="goHome">个人主页</el-dropdown-item>
                <el-dropdown-item command="logout" divided>退出</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </a>
        </li>
      </ul>
    </div>
    <el-dialog title="兴趣选择" :visible.sync="dialogFormVisible">
      <el-form>
        <el-form-item label="" :label-width="formLabelWidth">
          <el-checkbox-group v-model="checkbox" size="middle" class="checkvox">
            <el-checkbox label="喜剧" border style="margin-left:10px"></el-checkbox>
            <el-checkbox label="动作" border></el-checkbox>
            <el-checkbox label="犯罪" border></el-checkbox>
            <el-checkbox label="奇幻" border></el-checkbox>
            <el-checkbox label="剧情" border></el-checkbox>
            <el-checkbox label="冒险" border></el-checkbox>
            <el-checkbox label="家庭" border></el-checkbox>
            <el-checkbox label="爱情" border></el-checkbox>
            <el-checkbox label="同性" border></el-checkbox>
            <el-checkbox label="音乐" border></el-checkbox>
            <el-checkbox label="惊悚" border></el-checkbox>
            <el-checkbox label="情色" border></el-checkbox>
            <el-checkbox label="动画" border></el-checkbox>
            <el-checkbox label="歌舞" border></el-checkbox>
            <el-checkbox label="科幻" border></el-checkbox>
            <el-checkbox label="儿童" border></el-checkbox>
            <el-checkbox label="历史" border></el-checkbox>
            <el-checkbox label="战争" border></el-checkbox>
            <el-checkbox label="悬疑" border></el-checkbox>
            <el-checkbox label="传记" border></el-checkbox>
            <el-checkbox label="西部" border></el-checkbox>
            <el-checkbox label="恐怖" border></el-checkbox>
            <el-checkbox label="武侠" border></el-checkbox>
            <el-checkbox label="古装" border></el-checkbox>
            <el-checkbox label="灾难" border></el-checkbox>
            <el-checkbox label="黑色电影" border style="margin-right:0px;"></el-checkbox>
            <el-checkbox label="运动" border style="margin-right:32px;"></el-checkbox>
            <el-checkbox label="惊栗" border></el-checkbox>
            <el-checkbox label="悬念" border></el-checkbox>
            <el-checkbox label="荒诞" border></el-checkbox>
            <el-checkbox label="戏曲" border></el-checkbox>
            <el-checkbox label="鬼怪" border></el-checkbox>
            <el-checkbox label="达人秀" border style="margin-right:16px;"></el-checkbox>
            <el-checkbox label="搞笑" border></el-checkbox>
            <el-checkbox label="成人" border></el-checkbox>
            <el-checkbox label="舞台艺术" border style="margin-right:10px"></el-checkbox>
            <el-checkbox label="真人秀" border style="margin-right:16px"></el-checkbox>
            <el-checkbox label="脱口秀" border style="margin-right:16px"></el-checkbox>
            <el-checkbox label="访谈" border></el-checkbox>
            <el-checkbox label="纪录片" border></el-checkbox>
          </el-checkbox-group>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="cancel">取 消</el-button>
        <el-button type="primary" @click="selectInterests">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>
<script>
import axios from 'axios'
export default {
  name: 'Header',
  inject: ['routerRefresh'],
  data() {
    return {
      input: '',
      dialogFormVisible: false,
      formLabelWidth: '120px',
      checkbox: [],
      nickname: sessionStorage.getItem('username'),
      // 登录状态就显示下拉列表
      state: sessionStorage.getItem('username') == null ? true : false
    }
  },
  methods: {
    //搜索内容
    search() {
      if (this.input) {
        this.$router.push({ path: '/findmovie', query: { name: this.input } })
        this.input = ''
        this.routerRefresh()
      } else {
        this.$message.error('请先输入搜索内容')
      }
    },
    //点击logo返回主页
    returnHome() {
      // console.log(this.$route.path)
      if (this.$route.path != '/home') {
        this.$router.push('home')
      }
    },
    cancel() {
      this.dialogFormVisible = false
      this.checkbox = []
    },
    selectInterests() {
      this.dialogFormVisible = false
      if (this.checkbox.length != 0) {
        console.log(this.checkbox)
        axios.post('/api/chooseinterests', {
          userid: 'ls',
          interests: this.checkbox
        })
        this.checkbox = []
      }
    },
    chooseinterests() {
      if (sessionStorage.getItem('username')) {
        // console.log(sessionStorage.getItem('username'))
        this.dialogFormVisible = true
      } else {
        this.$router.push('/login')
      }
    },
    personalrecommend() {
      // /personalrecommend?userid=admin
      if (sessionStorage.getItem('username')) {
        console.log(sessionStorage.getItem('username'))
        this.$router.push(`/recommend?userid=${sessionStorage.getItem('username')}`)
      } else {
        this.$router.push('/login')
      }
    },
    handleCommand(command) {
      if (command == 'goHome') {
        // this.$message.success('goHome!')
        this.$router.push('userpage')
      } else {
        sessionStorage.removeItem('username')
        this.$message.success('您已退出登录!')
        this.$router.push('/home')
        this.routerRefresh()
      }
    }
  }
}
</script>
<style lang='less' scoped>
.el-dropdown-link {
  cursor: pointer;
  color: #050505;
  font-size: 18px;
}
.el-icon-arrow-down {
  font-size: 18px;
}
.header {
  height: 116px;
  // background-color: pink;
  margin: 5px auto;
}
.logo {
  float: left;
  height: 116px;
  width: 226px;
  // background-color: skyblue;
  cursor: pointer;
}
.nav {
  float: left;
  // margin-left: 60px;
}
.nav ul li {
  float: left;
  margin: 0 10px;
}
.nav ul li a {
  display: block;
  height: 116px;
  padding: 0px 5px;
  line-height: 116px;
  font-size: 18px;
  color: #050505;
  text-decoration: none;
}
.nav ul li a:hover {
  color: #00a4ff;
}
.search {
  float: left;
  width: 251px;
  height: 32px;
  margin-top: 43px;
  margin-left: 10px;
  // background-color: skyblue;
}
.search input {
  float: left;
  width: 180px;
  height: 30px;
  outline: medium;
  border: 1px solid #00a4ff;
  border-right: none;
  padding-left: 10px;
}
.search button {
  float: left;
  width: 50px;
  height: 32px;
  border: none;
  background: url(./images/btn.png);
}
.rightnav {
  margin-left: 20px;
}
.nav ul li .personalrecommend {
  color: red;
}
</style>