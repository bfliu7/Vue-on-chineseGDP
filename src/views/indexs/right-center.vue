<!--
 * @Author: daidai
 * @Date: 2022-03-01 14:13:04
 * @LastEditors: Please set LastEditors
 * @LastEditTime: 2022-09-27 15:04:49
 * @FilePath: \web-pc\src\pages\big-screen\view\indexs\right-top.vue
-->
<template>
  <Echart
    id="rightcenter"
    :options="option"
    class="right_top_inner"
    v-if="pageflag"
    ref="charts"
  />
  <Reacquire v-else @onclick="get_data" style="line-height: 200px">
    重新获取
  </Reacquire>
</template>

<script>
import { currentGET } from "api/modules";
import { graphic } from "echarts";
import * as echarts from "echarts";
export default {
  data() {
    return {
      lists: {
        dateList: [
          "1952",
          "1953",
          "1954",
          "1955",
          "1956",
          "1957",
          "1958",
          "1959",
          "1960",
          "1961",
        ],
        numList: [
          2.45, 1.88, 1.69, 7.92, 4.66, 3.07, 0.44, -15.86, -16.38, 1.45,
        ],
        numList2: [
          36.12, 35.82, 15.66, 7.58, 34.47, 8.04, 52.9, 25.79, 5.58, -42.07,
        ],
        numList3: [
          19.26, 24.85, -0.39, 4.83, 13.29, 4.67, 18.09, 15.57, 4.98, -25.84,
        ],
        numList4: [
          14.79, 15.62, 4.21, 6.85, 15.02, 5.06, 21.25, 8.82, -0.32, -27.32,
        ],
      },
      option: {},
      pageflag: false,
      isFullScreen: false,
    };
  },

  beforeMount() {
    this.init(
      this.lists.dateList,
      this.lists.numList,
      this.lists.numList2,
      this.lists.numList3,
      this.lists.numList4
    );
  },

  mounted() {
    this.get_data();
  },

  beforeDestroy() {
    this.clearData();
  },

  methods: {
    get_data() {
      //记得调用fn
      this.pageflag = true;
      this.$http
        .get("/right_center")
        .then((response) => {
          if (
            this.lists.dateList.length == response.data.dateList.length &&
            this.lists.dateList[0] == response.data.dateList[0]
          ) {
            console.log;
          } else {
            this.lists = response.data;
            this.init(
              this.lists.dateList,
              this.lists.numList,
              this.lists.numList2,
              this.lists.numList3,
              this.lists.numList4
            );
          }
          this.switper();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    switper() {
      if (this.timer) {
        return;
      }
      let looper = (a) => {
        // console.log(11111111111,lists)
        this.get_data();
      };
      this.timer = setInterval(looper, 1000); //1秒刷新一次
    },

    clearData() {
      if (this.timer) {
        clearInterval(this.timer);
      }
    },

    handleFull() {
      // 全屏按钮点击事件
      this.$emit("openn", this.isFullScreen);
    },

    init(xData, yData, yData2, yData3, yData4) {
      this.option = {
        legend: {
          data: [
            {
              name: "第一产业",
              textStyle: {
                color: "rgba(252,144,16,.7)", // 图例文字颜色
              },
            },
            {
              name: "第二产业",
              textStyle: {
                color: "rgba(9,202,243,.7)", // 图例文字颜色
              },
            },
            {
              name: "第三产业",
              textStyle: {
                color: "rgba(249,100,111,.7)", // 图例文字颜色
              },
            },
            {
              name: "总指数",
              textStyle: {
                color: "rgba(252,255,255,1)", // 图例文字颜色
              },
            },
          ],
        },
        xAxis: {
          name: "年",
          type: "category",
          data: xData,
          boundaryGap: false, // 不留白，从原点开始
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
            // formatter:'year'
          },
        },
        yAxis: {
          name: "%",
          show: true,
          type: "value",
          splitLine: {
            show: true,
            lineStyle: {
              color: "rgba(31,99,163,.2)",
            },
          },
          axisLine: {
            lineStyle: {
              color: "rgba(31,99,163,.1)",
            },
          },
          axisLabel: {
            color: "#7EB7FD",
            fontWeight: "500",
            formatter: "{value}%",
          },
        },
        tooltip: {
          trigger: "axis",
          backgroundColor: "rgba(0,0,0,.6)",
          borderColor: "rgba(147, 235, 248, .8)",
          textStyle: {
            color: "#FFF",
            fontSize: 15,
          },
          formatter: function (params) {
            var str =
              '<div style="color: white"><p>年代：' +
              params[0].name.split("[")[0] +
              "<p><div>";
            for (var i = 0; i < params.length; i++) {
              str +=
                params[i].marker +
                " " +
                params[i].seriesName +
                " ：" +
                params[i].value +
                "%<br>";
            }
            return str;
          },
        },
        grid: {
          //布局
          show: true,
          left: "20px",
          right: "20px",
          bottom: "5px",
          top: "22px",
          containLabel: true,
          borderColor: "#1F63A3",
        },
        series: [
          {
            data: yData,
            type: "line",
            smooth: true,
            symbol: "none", //去除点
            name: "第一产业",
            color: "rgba(252,144,16,.7)",
            areaStyle: {
              //右，下，左，上
              color: new graphic.LinearGradient(
                0,
                0,
                0,
                1,
                [
                  {
                    offset: 0,
                    color: "rgba(252,144,16,.7)",
                  },
                  {
                    offset: 0.4,
                    color: "rgba(252,144,16,.0)",
                  },
                ],
                false
              ),
            },
            // markPoint: {
            //   data: [
            //     {
            //       name: "最大值",

            //       type: "max",
            //       valueDim: "y",
            //       symbol: "rect",
            //       symbolSize: [60, 26],
            //       symbolOffset: [0, -20],
            //       itemStyle: {
            //         color: "rgba(0,0,0,0)",
            //       },
            //       label: {
            //         color: "#FC9010",
            //         backgroundColor: "rgba(252,144,16,0.1)",
            //         borderRadius: 6,
            //         padding: [7, 14],
            //         borderWidth: 0.5,
            //         borderColor: "rgba(252,144,16,.5)",
            //         formatter: "罗田主线站：{c}",
            //       },
            //     },
            //     {
            //       name: "最大值",
            //       type: "max",
            //       valueDim: "y",
            //       symbol: "circle",
            //       symbolSize: 6,
            //       itemStyle: {
            //         color: "#FC9010",
            //         shadowColor: "#FC9010",
            //         shadowBlur: 8,
            //       },
            //       label: {
            //         formatter: "",
            //       },
            //     },
            //   ],
            // },
          },
          {
            data: yData2,
            type: "line",
            smooth: true,
            symbol: "none", //去除点
            name: "第二产业",
            color: "rgba(9,202,243,.7)",
            areaStyle: {
              //右，下，左，上
              color: new graphic.LinearGradient(
                0,
                0,
                0,
                1,
                [
                  {
                    offset: 0,
                    color: "rgba(9,202,243,.7)",
                  },
                  {
                    offset: 0.4,
                    color: "rgba(9,202,243,.0)",
                  },
                ],
                false
              ),
            },
            // markPoint: {
            //   data: [
            //     {
            //       name: "最大值",
            //       type: "average",
            //       valueDim: "y",
            //       symbol: "rect",
            //       symbolSize: [60, 26],
            //       symbolOffset: [0, -20],
            //       itemStyle: {
            //         color: "rgba(0,0,0,0)",
            //       },
            //       label: {
            //         color: "#09CAF3",
            //         backgroundColor: "rgba(9,202,243,0.1)",

            //         borderRadius: 6,
            //         borderColor: "rgba(9,202,243,.5)",
            //         padding: [7, 14],
            //         formatter: "水朗D站：{c}",
            //         borderWidth: 0.5,
            //       },
            //     },
            //     {
            //       name: "最大值",
            //       type: "min",
            //       valueDim: "y",
            //       symbol: "circle",
            //       symbolSize: 6,
            //       itemStyle: {
            //         color: "#09CAF3",
            //         shadowColor: "#09CAF3",
            //         shadowBlur: 8,
            //       },
            //       label: {
            //         formatter: "",
            //       },
            //     },
            //   ],
            // },
          },
          {
            data: yData3,
            type: "line",
            smooth: true,
            symbol: "none", //去除点
            name: "第三产业",
            color: "rgba(249,100,111,.7)",
            areaStyle: {
              //右，下，左，上
              color: new graphic.LinearGradient(
                0,
                0,
                0,
                1,
                [
                  {
                    offset: 0,
                    color: "rgba(249,100,111,.7)",
                  },
                  {
                    offset: 0.4,
                    color: "rgba(249,100,111,.0)",
                  },
                ],
                false
              ),
            },
            // markPoint: {
            //   data: [
            //     {
            //       name: "最大值",
            //       type: "max",
            //       valueDim: "y",
            //       symbol: "rect",
            //       symbolSize: [60, 26],
            //       symbolOffset: [0, -20],
            //       itemStyle: {
            //         color: "rgba(0,0,0,0)",
            //       },
            //       label: {
            //         color: "rgba(249,100,111)",
            //         backgroundColor: "rgba(249,100,111,0.1)",

            //         borderRadius: 6,
            //         borderColor: "rgba(249,100,111,.5)",
            //         padding: [7, 14],
            //         formatter: "松山湖南：{c}",
            //         borderWidth: 0.5,
            //       },
            //     },
            //     {
            //       name: "最大值",
            //       type: "max",
            //       valueDim: "y",
            //       symbol: "circle",
            //       symbolSize: 6,
            //       itemStyle: {
            //         color: "rgba(249,100,111)",
            //         shadowColor: "rgba(249,100,111)",
            //         shadowBlur: 8,
            //       },
            //       label: {
            //         formatter: "",
            //       },
            //     },
            //   ],
            // },
          },
          {
            data: yData4,
            type: "line",
            smooth: true,
            symbol: "none", //去除点
            name: "总指数",
            color: "rgba(252,255,255,1)",
            areaStyle: {
              //右，下，左，上
              color: new graphic.LinearGradient(
                0,
                0,
                0,
                1,
                [
                  {
                    offset: 0,
                    color: "rgba(252,255,255,1)",
                  },
                  {
                    offset: 0.5,
                    color: "rgba(252,255,255,.0)",
                  },
                ],
                false
              ),
            },
            markPoint: {
              data: [
                {
                  name: "最大值",

                  type: "max",
                  valueDim: "y",
                  symbol: "rect",
                  symbolSize: [60, 26],
                  symbolOffset: [0, -20],
                  itemStyle: {
                    color: "rgba(0,0,0,0)",
                  },
                  label: {
                    color: "rgba(252,255,255,4)",
                    backgroundColor: "rgba(252,255,255,0.1)",
                    borderRadius: 6,
                    padding: [7, 14],
                    borderWidth: 0.5,
                    borderColor: "rgba(252,255,255,.5)",
                    formatter: "最大增速：{per|{c}%}",
                    rich: {
                      per: {
                        color: "white",
                        fontSize: 18,
                      },
                    },
                  },
                },
                {
                  name: "最大值",
                  type: "max",
                  valueDim: "y",
                  symbol: "circle",
                  symbolSize: 6,
                  itemStyle: {
                    color: "rgba(252,255,255,.5)",
                    shadowColor: "rgba(252,255,255,.9)",
                    shadowBlur: 8,
                  },
                  label: {
                    formatter: "",
                  },
                },
              ],
            },
          },
        ],
        toolbox: {
          feature: {
            myFull: {
              // 自定义全屏按钮
              show: true,
              title: "全屏",
              icon: "path://M432.45,595.444c0,2.177-4.661,6.82-11.305,6.82c-6.475,0-11.306-4.567-11.306-6.82s4.852-6.812,11.306-6.812C427.841,588.632,432.452,593.191,432.45,595.444L432.45,595.444z M421.155,589.876c-3.009,0-5.448,2.495-5.448,5.572s2.439,5.572,5.448,5.572c3.01,0,5.449-2.495,5.449-5.572C426.604,592.371,424.165,589.876,421.155,589.876L421.155,589.876z M421.146,591.891c-1.916,0-3.47,1.589-3.47,3.549c0,1.959,1.554,3.548,3.47,3.548s3.469-1.589,3.469-3.548C424.614,593.479,423.062,591.891,421.146,591.891L421.146,591.891zM421.146,591.891", // 省略部分代码，可自行选择或设计图标
              onclick: this.handleFull, // 全屏按钮点击事件
            },
          },
        },
      };
    },
  },
};
</script>
<style lang="scss" scoped>
.right_top_inner {
  // height: 100px;
  margin: 0px;
  padding: 0px;
  border: 0px;
}
</style>
