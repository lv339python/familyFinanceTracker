import {Home, Funds, Groups, Spendings, Incomes} from 'src/tabs';
import {Login, Spending_registration, Spend, Limit, Icon_getter, Spending_add, Financial_goal, Funds_registration, Spending_history, PasswordRecovery, Income_registration,  Income_tracker, Groups_registration, Goal, Income_add} from "src/components";


export default [
    //login
    {
        path: '/password_recovery', component: PasswordRecovery
    },
    {
        path: '/password_recovery/:token', component: PasswordRecovery
    },
    {
        path: '/', redirect: '/login'
    },
    //tabs
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
    //spending
    {
        path: '/spendings/add', component: Spending_registration
    },
    {
        path: '/spendings/limit_ind', component: Spend
    },
    {
        path: '/spendings/limit_group', component: Limit
    },
    {
        path: '/spendings/new', component: Spending_add
    },
    {
        path: '/spendings/history', component: Spending_history
    },
    //Group
    {
        path: '/groups/add', component: Groups_registration
    },

    //funds
    {
        path: '/funds/new', component: Funds_registration
    },
    {
        path: '/funds/new_goal', component:Financial_goal
    },
      {
        path: '/funds/tracking_goal', component: Goal
    },
    //incomes
    {
        path: '/incomes/tracking', component: Income_tracker
    },

    {
        path: '/incomes/add', component: Income_registration
    },

    {
        path: '/incomes/new', component: Income_add
    }
];
