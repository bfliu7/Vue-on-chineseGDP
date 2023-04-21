<!--
 * @Author: daidai
 * @Date: 2022-03-01 15:51:43
 * @LastEditors: Please set LastEditors
 * @LastEditTime: 2022-09-29 15:12:46
 * @FilePath: \web-pc\src\pages\big-screen\view\indexs\right-bottom.vue
-->
<template>
  <Echart id="leftBottom" :options="option" class='right_bottom' v-if="pageflag" ref="charts" />
  <Reacquire v-else @onclick="get_data" style="line-height: 200px">
    重新获取
  </Reacquire>
  

</template>

<script>
import * as echarts from "echarts";


export default {

  data() {
    return {
      lists:[["广东省","四川省","河南省","上海市","河北省","辽宁省","山东省","江苏省"],["14.39","21.18","22.46","2.17","25.23","12","28.55","25.49"],["6.7","4.55","8.23","19.22","7.61","20","7.87","8.53"],["8.43","5.96","5.4","15.27","7.65","9.38","6.99","14.39"]],
      option: {},
      pageflag: false,
      
    };
  },

  beforeMount() {
    this.init(this.lists[0],this.lists[1],this.lists[2],this.lists[3])
  },

  mounted() {
    this.get_data()
  },
  beforeDestroy() {
    this.clearData()
  },
  methods: {
    get_data() { //记得调用fn
      this.pageflag = true
      this.$http.get('/left_bottom')
        .then((response) => {
          if (this.lists[1][2] == response.data.list[1][2]) {
            console.log
          }
          else {
            this.lists = response.data.list
            this.init(this.lists[0],this.lists[1],this.lists[2],this.lists[3])
          }
          this.switper()
        })
        .catch((error) => {
          console.log(error);
          this.init
        });
    },


    clearData() {
      if (this.timer) {
        clearInterval(this.timer)
        this.timer = null
      }
    },
    //轮询
    switper() {
      if (this.timer) {
        return
      }
      let looper = (a) => {
        this.get_data()
      };
      this.timer = setInterval(looper, 1000);//this.$store.state.setting.echartsAutoTime
    },

    init(data,data1,data2,data3) {
      this.option = {
        legend: {
          data: [
            {
              name: "第一产业",
              textStyle: {
                color: "rgba(122, 122, 255, 1)", // 图例文字颜色
              },
            },
            {
              name: "第二产业",
              textStyle: {
                color: "rgba(207, 255, 243, 1)", // 图例文字颜色
              },
            },
            {
              name: "第三产业",
              textStyle: {
                color: "rgba(210, 100, 110, 1)", // 图例文字颜色
              },
            },

          ],
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            // Use axis to trigger tooltip
            type: 'shadow' // 'shadow' as default; can also be 'line' or 'shadow'
          },

          backgroundColor: "rgba(0,0,0,.6)",
          borderColor: "rgba(147, 235, 248, .8)",
          textStyle: {
            color: "#FFF",
            fontSize: 15,
          },
          formatter: function (params) {
            var str =
              '<div style="color: white"><p>省份：' +
              params[0].name.split("[")[0] +
              "<p><div>";
            for (var i = 0; i < params.length; i++) {
              str +=
                params[i].marker +
                " " +
                params[i].seriesName +
                " ：" +
                params[i].value +
                "亿<br>";
            }
            return str;
          },

        },
        grid: {
          //布局
          show: true,
          trigger: 'item',
          left: "20px",
          right: "20px",
          bottom: "15px",
          top: "22px",
          containLabel: true,
          borderColor: "#1F63A3",
        },
        textStyle:{
          color:'white'
        },
        xAxis: {
          type: 'value',
          splitLine: {
            show: true,
            lineStyle: {
              color: "rgba(31,99,163,.2)",
            },
          },
          axisLine: {
            // show:false,
            lineStyle: {
              color: "rgba(31,99,163,.1)",
            },
          },
          axisLabel: {
            color: "#7EB7FD",
            fontWeight: "500",
            formatter: "{value}亿",
          }
        },
        yAxis: {
          type: 'category',
          axisLine: {
            lineStyle: {
              color: "rgba(31,99,163,.1)",
            },
          },
          axisLabel: {
            color: "#7EB7FD",
            fontWeight: "500",
            formatter: "{value}",
          },
          data: data
        },
        series: [
          {
            name: '第一产业',
            type: 'bar',
            stack: 'total',
            label: {
              show: true,
              color:'white'
            },
            emphasis: {
              focus: 'series'
            },
            color: 'rgba(122, 122, 255, 1)',
            data: data1
          },
          {
            name: '第二产业',
            type: 'bar',
            stack: 'total',
            label: {
              show: true,
              color:'black'

            },
            emphasis: {
              focus: 'series'
            },
            color: 'rgba(207, 255, 243, 1)',
          
            data: data2
          },
          {
            name: '第三产业',
            type: 'bar',
            stack: 'total',
            label: {
              show: true,
              color:'white'

            },
            emphasis: {
              focus: 'series'
            },
            color: 'rgba(210, 100, 110, 1)',
            data: data3
          },

        ]
      };
    }


  },
};
</script>
<style lang='scss' scoped>
.right_bottom {
  box-sizing: border-box;
  padding: 0px;
  margin: 0px;


  .img_wrap {
    display: flex;
    // justify-content: space-around;
    box-sizing: border-box;
    padding: 0 0 20px;
    // overflow-x: auto;

    li {
      width: 105px;
      height: 137px;
      border-radius: 6px;
      overflow: hidden;
      cursor: pointer;
      // background: #84ccc9;
      // border: 1px solid #ffffff;
      overflow: hidden;
      flex-shrink: 0;
      margin: 0 10px;

      img {
        flex-shrink: 0;
      }
    }




  }

  .noData {
    width: 100%;
    line-height: 100px;
    text-align: center;
    color: rgb(129, 128, 128);
  }
}
</style>
