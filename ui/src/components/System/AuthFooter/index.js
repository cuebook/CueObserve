import React, { useState } from "react";

export default function Footer() {
        let newDate = new Date()
        let year = newDate.getFullYear();
        return (
            <div className="mt-auto pb-5 pt-5">
                {/* <ul
                className={`${style.footerNav} list-unstyled d-flex mb-2 flex-wrap justify-content-center`}
                >
                <li>
                    <a>Terms of Use</a>
                </li>
                <li>
                    <a>Compliance</a>
                </li>
                <li>
                    <a>Support</a>
                </li>
                <li>
                    <a>Contacts</a>
                </li>
                </ul> */}
                <div className="text-gray-4 text-center">© {year} Cuebook. All rights reserved.</div>
            </div>
        )
    }
