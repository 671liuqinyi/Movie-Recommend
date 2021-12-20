<template>
  <div id="char2" ref="chart" :style="{ width: '100%', height: '100%' }"></div>
</template>
<script>
import 'echarts-wordcloud/dist/echarts-wordcloud'
import 'echarts-wordcloud/dist/echarts-wordcloud.min.js'
import axios from 'axios'
export default {
  name: 'WordCloudChart',
  data() {
    return {
      username: sessionStorage.getItem('username'),
      worddata: [{ name: '喜剧', value: 1 }]
    }
  },
  async created() {
    let result1 = await axios.get('/api/wordcloud', {
      params: { username: this.username }
    })
    if (result1.data.msg == 'success') {
      this.worddata = result1.data.data
      this.initCharts() //初始化
    }
  },
  // mounted() {
  //   setTimeout(() => {
  //     this.initCharts() //初始化
  //   }, 0)
  // },
  methods: {
    initCharts() {
      let a = this.$refs.chart

      let myChart2 = this.$echarts.init(a)
      myChart2.setOption({
        title: {
          //text: "center"
        },
        backgroundColor: '#E6E6FA',
        tooltip: {},

        series: [
          {
            type: 'wordCloud',
            //用来调整词之间的距离
            gridSize: 10,
            // //用来调整字的大小范围

            sizeRange: [14, 60],
            // //用来调整词的旋转方向，，[0,0]--代表着没有角度，也就是词为水平方向，需要设置角度参考注释内容
            rotationRange: [-90, 90],
            // rotationRange: [ 0,90],
            // rotationRange: [0, 0],
            //随机生成字体颜色
            textStyle: {
              fontFamily: 'sans-serif',
              fontWeight: 'bold',
              // Color can be a callback function or a color string
              color: function () {
                // Random color
                return 'rgb(' + [Math.round(Math.random() * 160), Math.round(Math.random() * 160), Math.round(Math.random() * 160)].join(',') + ')'
              }
            },
            emphasis: {
              focus: 'self',

              textStyle: {
                shadowBlur: 10,
                shadowColor: '#333'
              }
            },
            //位置相关设置
            left: 'center',
            top: 'center',
            right: null,
            bottom: null,
            width: '200%',
            height: '200%',
            //数据
            data: this.worddata
          }
        ]
      })
      //点击事件
      myChart2.on('click', function (params) {
        alert(params.name)
      })
    }
  }
}
</script>
<style  scoped>
</style>