import Vue from 'vue'
import Router from 'vue-router'
import ScheduleRouter from '@/components/Schedule/Schedule-router'
import FrontPageRouter from '@/components/FrontPage/FrontPage-router'
import ItineraryRouter from '@/components/Itinerary/Itinerary-router'

Vue.use(Router)

export default new Router({
    routes: [
        {
            path: '/',
            name: 'frontpage',
            alias: ["/home"],
            component: FrontPageRouter
        },

        {
            path: '/schedule',
            name: 'schedule',
            component: ScheduleRouter
        },

        {
            path: '/itinerary',
            name: 'itinerary',
            component: ItineraryRouter
        }
    ]
})