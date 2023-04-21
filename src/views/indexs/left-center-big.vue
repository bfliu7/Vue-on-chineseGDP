<!--
 * @Author: daidai
 * @Date: 2022-03-01 14:13:04
 * @LastEditors: Please set LastEditors
 * @LastEditTime: 2022-09-27 15:04:49
 * @FilePath: \web-pc\src\pages\big-screen\view\indexs\right-top.vue
-->
<template>
  <div style="height: 100%">
    <div style="height: 80%">
      <Echart
        id="charts"
        :options="option"
        class="right_top_inner"
        v-if="pageflag"
        ref="charts"
      >
      </Echart>
    </div>

    <div style="height: 20%; margin: 10px">
      <a style="display: inline">
        <el-input
          style="display: inline"
          placeholder="Input"
          v-model="input"
          clearable
        ></el-input>
      </a>
      <a style="display: inline; width: 50px">
        <el-button
          icon="el-icon-search"
          class="el-button__inner"
          @click="chaxun"
        ></el-button>
      </a>
    </div>
  </div>
</template>

<script>
import { currentGET } from "api/modules";
import { graphic } from "echarts";
import * as echarts from "echarts";
export default {
  data() {
    return {
      input: "",
      want: 10,
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
    // this.$nextTick(() => {
    //   let myChart = this.$refs.charts;
    //   console.log(myChart)
    //   // myChart.on('click', (params) => {
    //   //   console.log(1111111)

    //   // });

    // })
  },

  beforeDestroy() {
    this.clearData();
  },

  methods: {
    chaxun() {
      if (+this.input > 9 && +this.input < 70) {
        this.want = parseInt(this.input, 10);
        this.$http
          .post("/right_center_big_post", { want: this.want - 1 })
          .then((res) => {
            if (res.data.success) {
              console.log;
            }
          })
          .catch((error) => {
            console.log(error);
            alert("connect to net");
          });

        // this.display = parseInt(this.input, 10)

        // location.reload()  不适合此处
      } else {
        alert("wrong, please input 10 -> 69 ");
      }
    },
    get_data() {
      //记得调用fn
      this.pageflag = true;
      this.$http
        .get("/right_center_big")
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

    // handleFull() {
    //   console.log(111111111)
    // },

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
                  symbolSize: 10,
                  itemStyle: {
                    color: "rgba(252,255,255,1)",
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
      };
    },
  },
};
</script>
<style lang="scss" scoped>
.right_top_inner {
  height: 100%;
  width: 100%;
  margin: 0px;
  padding: 0px;
  border: 0px;
}

::v-deep .el-input__inner {
  width: 100px;
  text-align: center;
  height: 50px;
  border-radius: 20px;
  background-color: transparent;
  border: 2px solid #5dade2;
  background: transparent;
  font-size: 20px;
  color: rgba(255, 255, 255, 0.8);
  margin-left: 45%;
  margin-top: 10px;
  margin-right: 10px;
  padding-left: 10px;
  padding-top: 0px;
}

::v-deep .el-button__inner {
  border-radius: 12px;
  background-color: transparent;
  border: 0px solid #5dade2;
  background: transparent;

  margin: 0px;
  font-size: 22px;
  color: rgba(255, 255, 255, 0.8);
  margin-top: 0px;
  margin-left: 0px;
  margin-right: 0px;
  padding: 0px;
}

::v-deep .el-button__inner:hover {
  background-color: transparent;
  border: 0px solid #5dade2;
  background: transparent;
  font-size: 24px;
  color: rgba(255, 255, 255, 1);
}

::v-deep .el-button__inner:active {
  background-color: transparent;
  color: rgb(231, 231, 241);
}

::v-deep .el-button__inner:focus {
  background-color: transparent;
  color: rgb(255, 255, 255);
}
</style>
