<template>
    <div>
        <div style="margin-top: 15px;">
            Bing搜索关键词：
            <div style="margin: 5px 0;"></div>
            <el-input placeholder="请输入内容" v-model="key" class="input-with-select">
            </el-input>
            组织：
            <div style="margin: 5px 0;"></div>
            <el-input placeholder="请输入内容" v-model="org" class="input-with-select">
                <el-button slot="append" icon="el-icon-search" @click="getWrong"></el-button>
            </el-input>
        </div>
        <div style="margin: 50px 0;"></div>
        <div style="margin: 5px 0;"></div>
        <el-table
            v-loading="loading"
            :data="info"
            border
            style="width: 80%">
            <el-table-column
            fixed
            prop="url"
            label="网址"
            width="200">
            </el-table-column>
            <el-table-column
            prop="org"
            label="组织"
            width="200">
            </el-table-column>
            <el-table-column
            prop="time"
            label="时间"
            width="200">
            </el-table-column>
            <el-table-column
            prop="status"
            label="状态"
            width="200">
            </el-table-column>
        </el-table>
    </div>
</template>

<script>
    import Schart from 'vue-schart';
    import bus from '../common/bus';
    import axios from 'axios';
    export default {
        name: 'dashboard',
        components: {
        },
        computed: {
        },
        created(){
        },
        data() {
            return {
                info:[{
                    url:"",
                    time:"",
                    status:"",
                    org:"",
                }],
                key:"",
                org:"",
                per:0,
                loading:false,
            }
        },
        methods: {
            getWrong(){
                var that = this;
                let para={
                    "key":this.key,
                    "org":this.org,
                }
                console.log(para)
                this.loading=true;
                axios.request({
                    url:"/api/gettest/",
                    method:"POST",
                    data:para,
            }).then(function(response){
                console.log(response.data);
                that.info=response.data;
                that.loading=false;
            });
            }
        }
    }

</script>


<style scoped>
    .el-row {
        margin-bottom: 20px;
    }

    .grid-content {
        display: flex;
        align-items: center;
        height: 100px;
    }

    .grid-cont-right {
        flex: 1;
        text-align: center;
        font-size: 14px;
        color: #999;
    }

    .grid-num {
        font-size: 30px;
        font-weight: bold;
    }

    .grid-con-icon {
        font-size: 50px;
        width: 100px;
        height: 100px;
        text-align: center;
        line-height: 100px;
        color: #fff;
    }

    .grid-con-1 .grid-con-icon {
        background: rgb(45, 140, 240);
    }

    .grid-con-1 .grid-num {
        color: rgb(45, 140, 240);
    }

    .grid-con-2 .grid-con-icon {
        background: rgb(100, 213, 114);
    }

    .grid-con-2 .grid-num {
        color: rgb(45, 140, 240);
    }

    .grid-con-3 .grid-con-icon {
        background: rgb(242, 94, 67);
    }

    .grid-con-3 .grid-num {
        color: rgb(242, 94, 67);
    }

    .user-info {
        display: flex;
        align-items: center;
        padding-bottom: 20px;
        border-bottom: 2px solid #ccc;
        margin-bottom: 20px;
    }

    .user-avator {
        width: 120px;
        height: 120px;
        border-radius: 50%;
    }

    .user-info-cont {
        padding-left: 50px;
        flex: 1;
        font-size: 14px;
        color: #999;
    }

    .user-info-cont div:first-child {
        font-size: 30px;
        color: #222;
    }

    .user-info-list {
        font-size: 14px;
        color: #999;
        line-height: 25px;
    }

    .user-info-list span {
        margin-left: 70px;
    }

    .mgb20 {
        margin-bottom: 20px;
    }

    .todo-item {
        font-size: 14px;
    }

    .todo-item-del {
        text-decoration: line-through;
        color: #999;
    }

    .schart {
        width: 100%;
        height: 300px;
    }

</style>
