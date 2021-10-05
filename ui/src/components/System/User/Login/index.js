import React, { useState } from "react";

import { Form, Input, Button } from "antd";
import { Link } from "react-router-dom";
import style from "./style.module.scss";
import Footer from "../../AuthFooter/index.js"
import userServices from "services/main/user.js"
import { UserOutlined, LockOutlined } from '@ant-design/icons';


export default function Login(props) {
const [email, setEmail] = useState('')
const [password, setPassword] = useState('')
const [loading, setLoading] = useState(false)
const [isLoggedInSuccesfull, setLoggedInSuccessfull] = useState(false)


  const  onFinish = event => {
    setLoading(true)
    setEmail(event.email)
    setPassword(event.password)
    loggedIn(event.email, event.password)

  }
  const loggedIn = async (email, password) =>{
    const response =  await userServices.login(email, password)
    if(response && response.success){
      setLoggedInSuccessfull(true)
      props.loggedIn(true)
    }
    setLoading(false)
  }

    return (
      <div className={style.auth}>
        <div className={style.loginLogo}
        >
          <img src="resources/images/cuebook.png" alt="Cuebook Logo" />
        </div>
      <div className={style.container}>
          <Form
            layout="vertical"
            hideRequiredMark
            onFinish={onFinish}
            className="mb-4"
          >
            <Form.Item
            name="email"
            label="Email"
            rules = {[   
              {
                type: 'email',
                message: 'The input is not valid E-mail!',
              },
              {
              required: true,
              message: 'Please input your Email!',
            },
            ]}
            hasFeedback
            >
                <Input
                  placeholder="Email"
                  type="email"
                  className={`${style.inputField}`}


                />
            </Form.Item>
            <Form.Item
              name = "password"
              label="Password"

              rules = {[

                {
                  required:true,
                  message: "Please input your Password !"
                }
              ]}
            >
                <Input
                  type="password"
                  placeholder="Password"
                  className={`${style.inputField}`}
                />
            </Form.Item>
            <Button
              type="primary"
              size="large"
              className={style.loginButton}
              htmlType="submit"
              loading={loading}
            >
              Login
            </Button>
          </Form>

        </div>
        <Footer />
      </div>
    );
  
}
