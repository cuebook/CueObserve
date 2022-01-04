import React, { useState, useEffect } from "react";
import { Form, Input, Button } from 'antd';
import style from "./style.module.scss";
import settingService from "services/settings";
const {TextArea} = Input;

export default function Schedule(){
	const [settings, setSettings] = useState(null);
	const [loader, setLoader] = useState(false)


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
		setLoader(true)
	   console.log('Success:', values);
	   updateSettings(values)

	 };

	const updateSettings = async (values) => {
		const data = await settingService.updateSettings(values)
		if (data){
			setLoader(false)
			getSettings()
		}
	}

	 const onFinishFailed = (errorInfo: any) => {
	   console.log('Failed:', errorInfo);
	 };

	const formItems = settings && settings.map(setting=>{
		switch(setting.details.properties.type){
			case "text":
				return <Form.Item
						key={setting.name}
						label={setting.name}
						name={setting.name}
						
						>
						<Input defaultValue={setting.value}
						type={setting.details.isEncrypted ? "password" : "text"}
						/>
						</Form.Item>
			case "textarea":
				return <Form.Item 
					  key={setting.name} 
					  label={setting.name} 
					  rules={setting.details.properties.rules}
					  name={setting.name}
					>
		
					<TextArea rows={2} 
					className={style.inputFileArea}
					defaultValue={setting.value}
					/>
				</Form.Item>
			default:
				return <Form.Item 
						key={setting.name} 
						label={setting.details.label} 
						rules={setting.details.properties.rules}
						name={setting.name}
						>
						<Input
						type={setting.details.isEncrypted ? "password" : "text"}
						className={style.inputArea}
						defaultValue={setting.value}
						/>
						</Form.Item>
	}
	})
	return (
		<div className="xl:w-9/12">
			<Form
			layout="vertical" 
			 name="settingScreenForm"
			//  labelCol={{ span: 8 }}
			//  wrapperCol={{ span: 16 }}
			//  initialValues={{ remember: true }}
			 onFinish={onFinish}
			 onFinishFailed={onFinishFailed}
			 hideRequiredMark

			>
			<div className={style.addSettingForm}>
				{formItems}
			</div>
			<div className={style.submitButton}>
				<Button
                icon=""
                type="primary"
                className="mr-2"
                htmlType="submit"
				loading={loader}
            >
                Save
            </Button>
				</div>
		    </Form>
		</div>
		)
}