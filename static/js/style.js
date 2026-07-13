fetch("/api/settings", {

    method:"POST",

    headers:{
        "Content-Type":"application/json"
    },

    body:JSON.stringify({

        tahun:2026,

        triwulan:3

    })

})
