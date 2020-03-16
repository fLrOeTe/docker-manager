import Vue from 'vue';
import Router from 'vue-router';

Vue.use(Router);

export default new Router({
    routes: [
        {
            path: '/',
            redirect: '/dashboard'
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
                    path: '/dashboard',
                    component: resolve => require(['../components/page/Dashboard.vue'], resolve),
                    meta: { title: 'All images' }
                },
                {
                    path: '/search',
                    component: resolve => require(['../components/page/Search.vue'], resolve),
                    meta: { title: 'Search & Pull' }
                }
            ]
        },
        {
            path: '*',
            redirect: '/404'
        }
    ]
})
