/** @odoo-module **/

import {
    Component,
    onWillStart,
    useState
} from "@odoo/owl";

import {
    registry
} from "@web/core/registry";

import {
    useService
} from "@web/core/utils/hooks";


console.log("DOCTOR DASHBOARD FILE LOADED");


class DoctorDashboard extends Component {


    setup(){

        this.orm = useService("orm");


        this.state = useState({
            doctor:{
                name:"",
                image:"",
                department:"",
                phone:"",
                experience:""
            },

            totalAppointments: 0,

            todayAppointments: 0,

            revenue: 0,

        });


        onWillStart(async()=>{
            await this.loadDoctor();

            await this.loadDashboard();

        });

    }



    async loadDashboard(){

        const appointments =
            await this.orm.searchRead(

                "hospital.appoinment",

                [
                    ["doctor_id.user_id","=",this.env.services.user.userId]
                ],

                [
                    "date",
                    "state",
                    "revenue"
                ]

            );


        this.state.totalAppointments =
            appointments.length;


        let today =
            new Date()
            .toISOString()
            .split("T")[0];


        this.state.todayAppointments =
            appointments.filter(
                appt => appt.date === today
            ).length;


        this.state.revenue =
            appointments.reduce(
                (sum,appt)=>
                sum + appt.revenue,
                0
            );

    }
    async loadDoctor(){

    const doctor =
        await this.orm.searchRead(

            "hospital.doctor",

            [],

            [
                "name",
                "image",
                "department_id",
                "phone",
                "experience_level"
            ],

            {
                limit:1
            }

        );


    if(doctor.length){

        this.state.doctor={

            name:doctor[0].name,

            department:
            doctor[0].department_id[1],

            phone:
            doctor[0].phone,

            experience:
            doctor[0].experience_level,

            image:
            doctor[0].image

        };

    }

}


}



DoctorDashboard.template =
"hospital_management.DoctorDashboard";



console.log("Registering Doctor Dashboard");


registry
    .category("actions")
    .add(
        "hospital_management.doctor_dashboard",
        DoctorDashboard
    );


console.log("Doctor Dashboard Registered");