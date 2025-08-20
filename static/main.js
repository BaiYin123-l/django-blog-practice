/*
 * Copyright (c) 2025. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
 * Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
 * Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
 * Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
 * Vestibulum commodo. Ut rhoncus gravida arcu.
 */
$(document).ready(function(){
    const is_active_flag = "link-secondary";
    let check = location.pathname.split("#")[0];
    if (check === "/"){
        document.querySelector("body > div > header > ul > li:nth-child(1) > a").classList.add(is_active_flag);
    } else if (check === "/about/") {
        document.querySelector("body > div > header > ul > li:nth-child(2) > a").classList.add(is_active_flag);
    } else if (check === "/review/") {
        document.querySelector("body > div > header > ul > li:nth-child(3) > a").classList.add(is_active_flag);
    }
})
