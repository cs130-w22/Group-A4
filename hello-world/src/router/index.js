import Vue from 'vue'
import Router from 'vue-router'
import ScheduleRouter from '@/components/Schedule/Schedule-router'
import FrontPageRouter from '@/components/FrontPage/FrontPage-router'
import ItineraryRouter from '@/components/Itinerary/Itinerary-router'
import PageNotFoundRouter from '@/components/Utils/PageNotFound-router'


let firstVisit = true;

FrontPageRouter.beforeRouteLeave = function (to, from, next) {
    if (firstVisit && (to.name == 'schedule' && to.params.location === undefined)) { // users do not provide any location on the first visit
        this.$refs.textField.showErrorMessage();
        return false;
    } else {
        next();
    }
}

Vue.use(Router)

export default new Router({
    routes: [
        {
            path: '/',
            name: 'home',
            alias: ['/home', '/frontpage'],
            component: FrontPageRouter,
        },

        {
            path: '/schedule',
            name: 'schedule',
            component: ScheduleRouter,
            beforeEnter: (to, from, next) => {
                if (firstVisit && to.params.location === undefined) { // users do not provide any location on the first visit
                    next('/home')
                } else {
                    firstVisit = false;
                    next();
                }
            }
        },

        {
            path: '/itinerary',
            name: 'itinerary',
            component: ItineraryRouter
        },
        {
            path: '/404',
            alias: ['*'],
            name: 'pageNotFound',
            component: PageNotFoundRouter,
        },
    ]
})