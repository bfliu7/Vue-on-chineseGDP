<!--
 * @Author: daidai
 * @Date: 2022-02-28 16:16:42
 * @LastEditors: Please set LastEditors
 * @LastEditTime: 2022-09-27 15:16:12
 * @FilePath: \web-pc\src\pages\big-screen\view\indexs\left-center.vue
-->
<template>
  <Echart id="leftCenter" :options="options" class="left_center_inner" v-if="pageflag" ref="charts" />
  <Reacquire v-else @onclick="getData" style="line-height:200px">
    重新获取
  </Reacquire>
</template>

<script>

export default {

  data() {

    return {
      options: {},
      countUserNumData: {
        lockNum: 342.9,
        onlineNum: 141.1,
        offlineNum: 195.1,
        totalNum: 679.1
      },
      pageflag: true,
      timer: null
    };
  },


  beforeMount() {
    this.init()
  },

  mounted() {
    this.get_data()
  },
  beforeDestroy() {
    this.clearData()

  },
  methods: {
    get_data() {
      this.$http.get('/left_center')
        .then((response) => {
          if ((this.countUserNumData.lockNum == response.data.lockNum) || !response.data) { console.log }
          else {
            this.countUserNumData = response.data
            this.init()
          }
          this.switper()

        })
        .catch(function (error) { console.log(error); });
    },
    switper() {
      if (this.timer) {
        return
      }
      let looper = (a) => {
        this.get_data()
      };
      this.timer = setInterval(looper, 1000);

    },

    clearData() {
      if (this.timer) {
        clearInterval(this.timer)
        this.timer = null
      }
    },
    // getData() {
    //   this.pageflag = true

    //   currentGET('big1').then(res => {
    //     //只打印一次
    //     if (!this.timer) {
    //       // console.log("left-center", res);
    //     }
    //     if (res.success) {
    //       // this.countUserNumData = res.data
    //       this.$nextTick(() => {
    //         // console.log(list)
    //         this.countUserNumData = this.list
    //         this.init()
    //         this.switper()
    //       })

    //     } else {
    //       this.pageflag = false
    //       this.$Message({
    //         text: res.msg,
    //         type: 'warning'
    //       })
    //     }
    //   })
    // },

    init() {
      let total = this.countUserNumData.totalNum;
      let colors = ["#ECA444", "#33A1DB", "#56B557"];
      let piedata = {
        name: "",
        type: "pie",
        radius: ["42%", "65%"],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 4,
          borderColor: "rgba(0,0,0,0)",
          borderWidth: 2,
        },

        color: colors,
        data: [

          {
            value: this.countUserNumData.lockNum,
            name: "第一产业",
            label: {
              shadowColor: colors[0],
            },
          },
          {
            value: this.countUserNumData.onlineNum,
            name: "第二产业",
            label: {
              shadowColor: colors[2],
            },
          },
          {
            value: this.countUserNumData.offlineNum,
            name: "第三产业",
            label: {
              shadowColor: colors[1],
            },
          },


        ],
      };
      this.options = {
        title: {
          // zlevel: 0,
          text: ["{value|" + parseInt(total, 10) + "}", "{name|亿}"].join("\n"),
          top: "center",
          left: "center",
          textStyle: {
            rich: {
              value: {
                color: "#ffffff",
                fontSize: 24,
                fontWeight: "bold",
                lineHeight: 20,
              },
              name: {
                color: "#ffffff",
                lineHeight: 20,
              },
            },
          },
        },
        tooltip: {
          trigger: "item",
          backgroundColor: "rgba(0,0,0,.6)",
          borderColor: "rgba(147, 235, 248, .8)",
          textStyle: {
            color: "#FFF",
            fontSize: 15
          },
          formatter: function (params) {
            var str = params.marker + " " + params.name + ":  " + params.value + "亿"
            return str
          }
        },
        legend: {
          show: false,
          top: "5%",
          left: "center",
        },

        series: [
          //展示圆点
          {
            ...piedata,
            radius:['40%','70%'],
            itemStyle: {
              borderRadius: 10,
              borderColor: 'black',
              borderWidth: 4

            },
            tooltip: { show: true },
            label: {
              formatter: "   {b|{b}}   \n   {c|{c}亿}  \n   {per|{d}%}  ",
              //   position: "outside",
              rich: {
                b: {
                  color: "#fff",
                  fontSize: 17,
                  lineHeight: 26,
                },
                c: {

                  color: "#31ABE3",
                  fontSize: 14,
                },
                per: {
                  color: "#31ABE3",
                  fontSize: 15,
                },
              },
            },
            labelLine: {
              length: 20, // 第一段线 长度
              length2: 30, // 第二段线 长度
              show: true,

            },
            emphasis: {
              show: true,
            },
          },
          {
            ...piedata,
            radius:['40%','70%'],
            itemStyle: {
              borderRadius: 10,
              borderColor: 'black',
              borderWidth: 4

            },
            tooltip: { show: true },
            
            label: {
              backgroundColor: "inherit", //圆点颜色，auto：映射的系列色
              height: 0,
              width: 0,
              lineHeight: 0,
              borderRadius: 2.5,
              shadowBlur: 8,
              shadowColor: "auto",
              padding: [2.5, -2.5, 2.5, -2.5],
            },
            labelLine: {
              length: 20, // 第一段线 长度
              length2: 30, // 第二段线 长度
              show: false,
            },
          },
        ],
      };
    },
  },
};
</script>
<style lang='scss' scoped></style>