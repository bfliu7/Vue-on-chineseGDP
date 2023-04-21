<template>
    <div>
        <div style="color: transparent;">,, </div>
        <div style="color: transparent;">,, </div>
        <div>
            <h1 class="div1">— {{ this.display }} —</h1>

            <div style="color: transparent;">-- </div>

            <a style="display: inline;">
                <el-input placeholder="Input" v-model="input" clearable></el-input>
            </a>

            <a style="display: inline;">
                <el-button icon="el-icon-search" class="el-button__inner" @click="chaxun"></el-button>
            </a>
            <a style="display: inline;">
                <el-button icon="el-icon-video-play" class="el-button__inner1" @click="lunxun"></el-button>
            </a>
        </div>
    </div>
</template>
<script>

export default {
    data() {
        return {
            display: 1952,
            input: '', //展示的时间
            want: 1952, //想要的时间
            startorstop: false //控制启停,true启false停
        }
    },
    methods: {
        chaxun() {
            if (+this.input > 1951 && +this.input < 2021) {
                this.clearData() // 消除loop影响
                this.startorstop = false //让自动轮询暂停
                this.want = parseInt(this.input, 10)
                this.$http.post('/left_top_search', { want: this.want, chaxun: 1 })
                    .then((res) => {
                        this.display = parseInt(this.input, 10)
                    }).catch((error) => {
                        console.log(error);
                        alert('connect to net');
                    })


                // this.display = parseInt(this.input, 10)

                // location.reload()  不适合此处
            }
            else {
                alert('wrong, please input 1952 -> 2020 ')
            }
        },

        ensure_consistence() {
            if (this.startorstop) { this.display = this.display + 1 }
            console.log
        },
        lunxun() {
            this.startorstop = !this.startorstop
            console.log('this.startorstop', this.startorstop)
            if (this.display == 2020) { this.startorstop = false }
            if (this.startorstop == true) {
                this.$http.post('/left_top_search', { want: this.display + 1, chaxun: 0 }).then((res) => {
                    console.log('left_top_lunxun', res.data.success)
                    console.log('this.display', this.display)
                    setTimeout(this.ensure_consistence(), 1000) //保证一致
                    // this.ensure_consistence()



                    this.switper()
                }).catch((error) => {
                    alert('connect to net'); this.startorstop = false;
                })

            }
            else {
                this.clearData()
            }

        },
        clearData() {
            if (this.timer) {
                clearInterval(this.timer);
                this.timer = null;
            }
        },
        switper() {
            if (this.timer) {
                return
            }
            let looper = (a) => {
                // this.display = this.display-1
                this.startorstop = !this.startorstop //此处这个looper函数，某种程度上来说就是后置一个相同函数然后去执行，于是必须得加个这个
                this.lunxun()
            };
            this.timer = setInterval(looper, 3000); //3秒刷新一次
        },
    },


}
</script>



<style scoped>
::v-deep .el-input__inner {
    width: 110px;
    height: 60px;
    border-radius: 20px;
    background-color: transparent;
    border-right: 2px solid #5DADE2;
    border-left: 2px solid #5DADE2;
    border-top: 2px solid #5DADE2;
    border-bottom: 2px solid #5DADE2;
    background: transparent;
    font-size: 20px;
    color: rgba(255, 255, 255, 0.8);
    margin-left: 195px;
    margin-right: 0px;
    padding-left: 30px;
    padding-top: 5px;

}

::v-deep .el-button__inner {

    border-radius: 12px;
    background-color: transparent;
    border: 0px solid #5DADE2;
    background: transparent;

    margin: 0px;
    font-size: 22px;
    color: rgba(255, 255, 255, 0.8);
    margin-top: 15px;
    margin-left: 215px;
    margin-right: 0px;
    padding: 0px;
}

::v-deep .el-button__inner:hover {
    background-color: transparent;
    border: 0px solid #5DADE2;
    background: transparent;
    font-size: 24px;
    color: rgba(255, 255, 255, 1)
}

::v-deep .el-button__inner:active {
    background-color: transparent;
    color: rgb(231, 231, 241);
}

::v-deep .el-button__inner:focus {
    background-color: transparent;
    color: rgb(255, 255, 255);

}

::v-deep .el-button__inner1 {
    width: 0px;
    height: 0px;
    border-radius: 12px;
    background-color: transparent;
    border: 0px solid #5DADE2;
    background: transparent;
    font-size: 22px;
    color: rgba(255, 255, 255, 0.8);
    margin-left: 30px;
    margin-right: 0px;

    padding: 0px;
}

::v-deep .el-button__inner1:hover {
    background-color: transparent;
    border: 0px solid #5DADE2;
    background: transparent;
    font-size: 24px;
    color: rgba(255, 255, 255, 1)
}

::v-deep .el-button__inner1:active {
    background-color: transparent;
    color: rgb(231, 231, 241);
}

::v-deep .el-button__inner1:focus {
    background-color: transparent;
    color: rgb(255, 255, 255);

}



.h11 {
    font-family: Arial, Helvetica, sans-serif;
    font-size: 80px;
    color: #ffffffe3;
    text-align: center;

}

.p1 {
    margin-top: 0px;
    padding-top: 0%;
    font-size: 45px;
    text-align: center;
}

.div1 {
    font-family: Arial, Helvetica, sans-serif;
    font-size: 80px;
    color: #ffffffe3;
    text-align: center;
    /* font-size: 2.5rem; */
    -webkit-animation: shining 2s alternate infinite;
    animation: shining 2s alternate infinite;
}

@-webkit-keyframes shining {
    from {
        text-shadow: 0 0 10px lightblue, 0 0 10px lightblue, 0 0 15px lightblue, 0 0 25px skyblue, 0 0 34px skyblue, 0 0 40px skyblue;
    }

    to {
        text-shadow: 0 0 5px lightblue, 0 0 5px lightblue, 0 0 10px lightblue, 0 0 15px skyblue, 0 0 18px skyblue, 0 0 24px skyblue;
    }
}
</style>
