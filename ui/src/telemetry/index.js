import React, { useState, useEffect, useRef } from "react";
import { Button, Form, Input, message, Select } from "antd";
import Analytics from 'analytics'
import segmentPlugin from '@analytics/segment'
import installationServices from "services/installation.js"

export const analytics = Analytics({
  app: 'CueObserve',
  plugins: [
    segmentPlugin({
      writeKey: 'Ap3yeUlzhDpVeGH0hXAJjaWZbZnQzp9x'
    })
  ]
})

export const telemetry = () => {

  let installationId = null
  const initiateTelemetry = async() => {
    const response = await installationServices.getInstallationId()
    if (response && response.success == true){
      installationId = response.data["installationId"]
      analytics.identify({
        "installationId":installationId,
      })
    }
    else if (response && response.success == false){
      analytics.identify({
        "installationId":"UnIdentified",
      })
    }
  }
  initiateTelemetry()
}
/* Track a page view */
// analytics.page()

/* Track a custom event */
// analytics.track( {
//   installationId:"7C35C4PZ5MCIJTT8"
// })

/* Identify a visitor */
// analytics.identify( {
//   installationId:"7C35C4PZ5MCIJTT8"
// })










