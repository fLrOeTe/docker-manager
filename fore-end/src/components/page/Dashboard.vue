<template>
    <el-row>
        <el-col :span="8" v-for="o in tableData" :key="o" :offset="0">
            <el-card class="box-card" :id="o">
                <div slot="header" class="clearfix">
                    <span><h4>{{ o.name }}</h4></span>
                    <el-button style="float: right; padding: 3px 0" type="text">setting</el-button>
                    <el-button style="float: right; padding: 3px 0" type="text" @click="getData(o)">delete</el-button>
                </div>
                <div class="text item">
                    <b>name:</b>{{ o.name}}
                </div>
                <div class="text item">
                    <b>tag:</b>{{ o.tag}}
                </div>
                <div class="text item">
                    <b>id:</b>{{ o.id}}
                </div>
                <div class="text item">
                    <b>time:</b>{{ o.time}}
                </div>
                <div class="text item">
                    <b>size:</b>{{ o.size+'b'}}
                </div>
            </el-card>
        </el-col>
    </el-row>
</template>
<script>
    import Schart from 'vue-schart';
    import bus from '../common/bus';
    import axios from 'axios';
    export default {
        data() {
            return {
                tableData: []
            }
        },
        created(){
            var that=this;
            axios.request({
                url:"/images/all/",
                method:"GET",
                responseType:"json"
            })
            .then(function(response){
                console.log(response.data);
                that.tableData=response.data;
            });
        },
        methods:{
            getData(index){
                console.log(index);
                axios.post("/images/delete/",index)
                .then(function(response){
                    console.log(response.data)
                    this.$router.go(0)
                });
            }
        }
    };
</script>
<style>
  .text {
    font-size: 14px;
  }

  .item {
    margin-bottom: 18px;
  }

  .clearfix:before,
  .clearfix:after {
    display: table;
    content: "";
  }
  .clearfix:after {
    clear: both
  }

  .box-card {
    width: 480px;
  }
</style>