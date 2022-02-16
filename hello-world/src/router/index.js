import Vue from 'vue'
import Router from 'vue-router'
import ScheduleRouter from '@/components/Schedule/Schedule-router'
import FrontPageRouter from '@/components/FrontPage/FrontPage-router'


Vue.use(Router)

export default new Router({
    routes: [
        {
            path: '/schedule',
            name: 'schedule',
            component: ScheduleRouter
        },

        {
            path: '/map',
            name: 'map',
            component: FrontPageRouter
        },

        {
            path: '/',
            name: 'frontpage',
            component: FrontPageRouter
        },
    ]
})