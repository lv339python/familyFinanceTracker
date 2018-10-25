import {Home, Funds, Groups, Spendings, Incomes} from 'src/tabs';
import {Login, Spending_registration, Spend, Limit, Icon_getter, Spending_add, Financial_goal, Funds_registration, Spending_history, PasswordRecovery, Income_registration,  Income_tracker, Groups_registration, Goal, Income_add} from "src/components";


export default [
    {
        path: '/', redirect: '/login'
    },
    {
        path: '/incomes', component: Incomes
    },
    {
        path: '/home', component: Home
    },
    {
        path: '/funds', component: Funds
    },
    {
        path: '/groups', component: Groups
    },
    {
        path: '/spendings', component: Spendings
    },
    {
        path: '/login', component: Login
    },
    {
        path: '/Spending_registration', component: Spending_registration
    },
    {
        path: '/spend', component: Spend
    },
    {
        path: '/limit', component: Limit
    },
    {
        path: '/add_spending', component: Icon_getter
    },
    {
        path: '/spending_add', component: Spending_add
    },
    {
        path: '/Financial_goal', component:Financial_goal
    },
    {
        path: '/funds_registration', component: Funds_registration
    },
    {
         path: '/spending_history', component: Spending_history
    },
    {
         path: '/track_incomes', component: Income_tracker
    },
    {
        path: '/password_recovery', component: PasswordRecovery
    },
    {
        path: '/groups_registration', component: Groups_registration
    },
    {
        path: '/password_recovery/:token', component: PasswordRecovery
    },
    {
        path: '/Income_registration', component: Income_registration
    },
    {
        path: '/goal', component: Goal
    },
    {
        path: '/income_add', component: Income_add
    }
];
