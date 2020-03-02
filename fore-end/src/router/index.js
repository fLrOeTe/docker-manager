import Vue from 'vue';
import Router from 'vue-router';

Vue.use(Router);

export default new Router({
    routes: [
        {
            path: '/',
            redirect: '/image'
        },
        {
            path: '/',
            component: resolve => require(['../components/common/Home.vue'], resolve),
            meta: { title: '自述文件' },
            children:[
                {
                    path: '/image',
                    component: resolve => require(['../components/page/ImageConfig.vue'], resolve),
                    meta: { title: '系统首页' }
                },
                {
                    path: '/search',
                    component: resolve => require(['../components/page/DownloadImage.vue'], resolve),
                    meta: { title: '查询修改' }
                }
            ]
        },
        {
            path: '*',
            redirect: '/404'
        }
    ]
})
