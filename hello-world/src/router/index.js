import Vue from 'vue'
import Router from 'vue-router'
import ScheduleRouter from '@/components/Schedule/Schedule-router'
import FrontPageRouter from '@/components/FrontPage/FrontPage-router'
import ItineraryRouter from '@/components/Itinerary/Itinerary-router'
import PageNotFoundRouter from '@/components/Utils/PageNotFound-router'
import ItineraryTabItemRouter from '@/components/Itinerary/ItineraryTabItem-router'

import axios from 'axios'

let firstVisit = true;
let prevItineraryId = -1;

FrontPageRouter.beforeRouteLeave = function (to, from, next) {
    if (firstVisit && (to.name == 'schedule' && to.params.location === undefined)) { // users do not provide any location on the first visit
        this.$refs.textField.showErrorMessage();
        return false;
    } else {
        next();
    }
}

ItineraryTabItemRouter.beforeRouteLeave = function (to, from, next) {
    prevItineraryId = this.id;
    next();
}

ItineraryRouter.beforeRouteEnter = function (to, from, next) {
    const access_token = Vue.cookie.get('access_token')

    if (access_token === null) { // user does not has access token, show this page with overlay
        next();
    }
    else if (prevItineraryId !== -1) { // user was previously visiting a tab and navigated away, using saved tab id to restore the old tab
        const saveItineraryId = prevItineraryId
        prevItineraryId = -1;

        next("/itinerary/" + saveItineraryId)
    }
    else { // user has access token, fetch the menu for him
        next(vm => {
            const headers = {
                'Content-Type': 'application/json',
                Authorization: 'Bearer ' + access_token,
            };
            axios
                .get('http://127.0.0.1:8000/trip/itinerary/', {
                    headers,
                })
                .then((resp) => {
                    const itinerarys = resp.data;
                    const ItineraryTabs = vm.$refs.ItineraryTabs;
                    ItineraryTabs.itinerarys = itinerarys

                    // user was previously visiting a tab and refreshed the page, using param to restore the old tab
                    const activeTabId = Number(to.params.id)
                    ItineraryTabs.tab = itinerarys.findIndex((e => e.id === activeTabId));

                    // tab might be -1, in this case, ItineraryTabItemRouter would redirect to 404
                })
                .catch((err) => {
                    console.error(err);
                });
        })
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
            component: ItineraryRouter,
            children: [
                {
                    path: ':id',
                    component: ItineraryTabItemRouter,
                    props: true
                },
            ],
        },

        {
            path: '/404',
            alias: ['*'],
            name: 'pageNotFound',
            component: PageNotFoundRouter,
        },
    ]
})