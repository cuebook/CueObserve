import React, { useState, useEffect } from "react";
import { Form, Input, Button } from 'antd';

import settingService from "services/settings";


export default function Schedule(){
	const [settings, setSettings] = useState(null);


	useEffect(()=>{
		if (!settings){
			getSettings();
		}
	}, []);

	const getSettings = async () => {
		const data = await settingService.getSettings()
		if (data){
			setSettings(data)
		}
	}

	const onFinish = (values) => {
	   console.log('Success:', values);
	   updateSettings(values)

	 };

	const updateSettings = async (values) => {
		const data = await settingService.updateSettings(values)
		if (data){
			getSettings()
		}
	}

	 const onFinishFailed = (errorInfo: any) => {
	   console.log('Failed:', errorInfo);
	 };

	const formItems = settings && settings.map(setting=>{
		return <Form.Item
					label={setting.name}
					name={setting.name}
				>
					<Input defaultValue={setting.value}/>
				</Form.Item>
	})

	return (
		<div className="xl:w-9/12">
			<Form
			 name="basic"
			 labelCol={{ span: 8 }}
			 wrapperCol={{ span: 16 }}
			 initialValues={{ remember: true }}
			 onFinish={onFinish}
			 onFinishFailed={onFinishFailed}
			>
				{formItems}

				<Form.Item wrapperCol={{ offset: 8, span: 16 }}>
				<Button type="primary" htmlType="submit">
				 Save
				</Button>
				</Form.Item>
		    </Form>
		</div>
		)
}