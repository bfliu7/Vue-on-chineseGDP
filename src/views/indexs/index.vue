<!--
 * @Author: daidai
 * @Date: 2022-03-04 09:23:59
 * @LastEditors: Please set LastEditors
 * @LastEditTime: 2022-05-07 11:05:02
 * @FilePath: \web-pc\src\pages\big-screen\view\indexs\index.vue
-->
<template link href="//netdna.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet">
  <div class="contents">
    <div class="contetn_left">
      <div class="pagetab">
        <!-- <div class="item">实时监测</div> -->

      </div>

      <ItemWrap class="contetn_left-top contetn_lr-item" title="数据查询">


        <LeftTop />

      </ItemWrap>
      <ItemWrap class="contetn_left-center contetn_lr-item" title="产业总览">
        <LeftCenter />
      </ItemWrap>
    <ItemWrap class="contetn_left-bottom contetn_lr-item" title="GDP前八名" style="padding: 0 10px 16px 10px">
      <LeftBottom />
      </ItemWrap>
    </div>
    <div class="contetn_center">
      <CenterMap class="contetn_center_top" />
      <!-- <ItemWrap class="contetn_center-bottom" title="24小时车辆情况">
                                      <CenterBottom />
                                    </ItemWrap> -->
    </div>
    <div class="contetn_right">
      <ItemWrap class="contetn_left-bottom contetn_lr-item" title="近十年GDP增速">
        <RightTop />
      </ItemWrap>
      <ItemWrap class="contetn_left-bottom contetn_lr-item" title="近十年GDP增速" style="padding: 0 10px 16px 10px">
        <RightCenter ref="RightCenter" @openn="openn" />
      </ItemWrap>
      <ItemWrap class="contetn_left-bottom contetn_lr-item" title="实时报警">
        <RightBottom />
      </ItemWrap>
    </div>



    <el-dialog :visible.sync="menuRoleVisible" append-to-body>
      <menu-role v-if="menuRoleVisible" ref="menuRole"></menu-role>
    </el-dialog>

  
  </div>
</template>

<script>
import LeftTop from './left-top.vue'
import LeftCenter from "./left-center.vue";
import LeftBottom from "./left-bottom.vue";
import CenterMap from "./center-map.vue";
import CenterBottom from "./center-bottom.vue";
import RightTop from "./right-top.vue";
import RightCenter from "./right-center.vue";
import RightBottom from "./right-bottom.vue";
import MenuRole from './right-center-big.vue';

export default {
  components: {
    LeftTop,
    LeftCenter,
    LeftBottom,
    CenterMap,
    RightTop,
    RightCenter,
    RightBottom,
    CenterBottom,
    MenuRole
  },
  data() {
    return {
      menuRoleVisible: false
    }
  },
  filters: {
    numsFilter(msg) {
      return msg || 0;
    },
  },
  created() {
  },

  mounted() { },
  methods: {
    openn(data) {
      if (data == false) {
        this.menuRoleVisible = true
      }
    }
  },
};

</script>
<style lang="scss" scoped>
// 内容
.contents {

  .contetn_left,
  .contetn_right {
    width: 540px;
    box-sizing: border-box;
    // padding: 16px 0;
  }

  .contetn_center {
    width: 720px;
  }

  //左右两侧 三个块
  .contetn_lr-item {
    height: 310px;
  }

  .contetn_center_top {
    width: 100%;
  }

  // 中间
  .contetn_center {
    display: flex;
    flex-direction: column;
    justify-content: space-around;
  }

  .contetn_center-bottom {
    height: 315px;
  }

  //左边 右边 结构一样
  .contetn_left,
  .contetn_right {
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    position: relative;

  }
}

::v-deep .v-modal {
  background-color: transparent;
}

::v-deep .el-dialog__wrapper {
  
  color: transparent;
  border: 0;
  height: 10px;
}

::v-deep .el-dialog {
  
  background-color: transparent;
  border: 0;
  height: 10px;
}

::v-deep .el-dialog__title {
  padding-bottom: 100px;
  background-color: transparent;
  border: 0;
  height: 10px;
}

::v-deep .el-dialog__headerbtn {
  padding-bottom: 100px;
  background-color: transparent;
  border: 0;
  height: 10px;
}

::v-deep .el-dialog__header {
  color: transparent;
  background-color: rgba(0, 0, 0, 0.7);
  border-top-left-radius: 100px;
  border-top-right-radius: 100px;
  border: 0;
  height: 10px;
}

::v-deep .el-dialog__body {
  background-color: rgba(0, 0, 0, 0.9);
  border-bottom-left-radius: 40px;
  border-bottom-right-radius: 40px;
  border: 0;
  height: 450px;
}

@keyframes rotating {
  0% {
    -webkit-transform: rotate(0) scale(1);
    transform: rotate(0) scale(1);
  }

  50% {
    -webkit-transform: rotate(180deg) scale(1.1);
    transform: rotate(180deg) scale(1.1);
  }

  100% {
    -webkit-transform: rotate(360deg) scale(1);
    transform: rotate(360deg) scale(1);
  }
}
</style>
