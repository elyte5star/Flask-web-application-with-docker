var entry_list = [];
class Entry {
    constructor(id, name, tel) {
        this.id = id;
        this.name = name;
        this.tel = tel;
        this.display = display_Entry;
    }
}
async function postData(url = "", data = {}) {
    let options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json; charset=utf-8"
        },
        body: JSON.stringify(data),
    };
    const response = await fetch(url, options);
    return response.json();
}

async function getData(url = "", data = {}) {
    let options = {
        method: "GET",
        headers: {
            "Content-Type": "application/json"

        },
    };
    const response = await fetch(url, options);
    return response.json();
}

function display_Entry(index) {
    return (
        '<div class="contact_id">' +
        "</div>\n" +
        '<div class="contact_name">' +
        "Name : " +
        this.name +
        "</div>\n" +
        '<div class="contact_tel">' +
        "Telephone : " +
        this.tel +
        "</div>\n" +
        '<div class="contact_operations">' +
        '<a href="javascript:void(0);" onclick="update_Entry(' +
        index +
        ')"><i class="fa fa-pencil-square-o"></i></a><br />' +
        '<a href="javascript:void(0);" onclick="delete_Entry(' +
        index +
        ')"><i class="fa fa-trash-o"></i></a>' +
        "</div>"
    );
}

/* get list of ppl */
async function get_ppl() {
    entry_list = [];
    const returned_result = await getData("/get_ppl").then((result) => {
        for ([key, val] of Object.entries(result.data)) {
            var person = new Entry(key, val[0], val[1]);
            entry_list.push(person);
        }

    });
    var contactsDiv = document.getElementById("list");
    contactsDiv.innerHTML = "";
    for (var i = 0; i < entry_list.length; i++) {
        var entryDiv = document.createElement("div");
        entryDiv.innerHTML =
            '<div id="contact_' +
            i +
            '" class="contact">' +
            entry_list[i].display(i) +
            "</div>";
        contactsDiv.appendChild(entryDiv);
    }
}

async function delete_Entry(idx) {
    const willDelete = await swal({
        title: "Are you sure you want to delete: Name: " + entry_list[idx].name + " with Tel: " + entry_list[idx].tel,
        text: "You won't be able to revert this!",
        icon: "warning",
        dangerMode: true,
        closeOnClickOutside: false,
        buttons: {
            cancel: {
                text: "No, cancel!",
                visible: true,
            },
            confirm: {
                text: "Yes, delete it!",
            },
        },
    });
    if (willDelete) {
        let obj = { "id": entry_list[idx].id }
        postData("/remove_person", obj).then((result) => {
            console.log(result.msg);
            Swal.fire({
                icon: "success",
                title: entry_list[idx].name + " has been deleted!",
                showConfirmButton: false,
                timer: 1200,
            });
            get_ppl();

        });

    } else {
        swal("This person's record is safe!");
    }
}

function login(){
    var userName = document.getElementById("username").value;
    var passWord = document.getElementById("pass").value;
    var obj ={"username":userName,"password":passWord};
    postData("./auth", obj).then((result) => {

        if (result.state){

        window.open(result.url , "_self" );
        
        $("#user_id").html(result.id);

        }else{

            $("#info2").html("Invalid Credentials. Please log in again.");

        }

    });

}

function update_Entry(idx) {
    $("#update_name").val(entry_list[idx].name);
    $("#update_tel").val(entry_list[idx].tel);
    $("#update_idx").val(idx);
    show_update_entry("update_entry");
}

function add_entry() {
    var name = $("#add_name").val().trim();
    var tel = $("#add_tel").val().trim();
    if (!is_Input_Error(name, tel)) {
        var obj = { name: name, number: tel };
        postData("/add_person", obj).then((result) => {
            Swal.fire({
                icon: "success",
                title: name + " has been added!",
                showConfirmButton: false,
                timer: 1200,
            });
        });

        hide_add_entry("add_entry");
    }
    get_ppl();
}


function make_changes() {
    var name = $("#update_name").val().trim();
    var tel = $("#update_tel").val().trim();
    var idx = $("#update_idx").val();
    var uniq_Id = entry_list[idx].id;
    if (!is_Input_Error(name, tel)) {
        var data = { _id: uniq_Id, name: name, number: tel };
        postData("/update_entity", data).then((result) => {
            get_ppl();
            console.log(result.msg);
        });
        hide_add_entry("update_entry");
    }
}

/* Helper functions */

function redirect() {
    window.location.href = "/";
}

function hide_update_entry(id) {
    var element = document.getElementById(id);
    element.style.display = "none";
}

function show_update_entry(id) {
    var element = document.getElementById(id);
    element.style.display = "";
}

function hide_add_entry(id) {
    var element = document.getElementById(id);
    element.style.display = "none";
}

function show_add_entry(id) {
    var name = $("#add_name").val(" ");
    var tel = $("#add_tel").val(" ");
    var element = document.getElementById(id);
    element.style.display = "";
}

function is_valid_Tel(tel) {
    var re = /^[0-9()+\-\s]*$/;
    return re.test(tel);
}

function is_valid_letter(name) {
    var re = /^[A-Za-z]+$/;
    return re.test(name);
}

function is_Input_Error(name, tel) {
    if (name.length == 0) {
        alert("Empty name!");
    } else if (tel.length == 0) {
        alert("Empty telephone number!");
    }
    // check for valid tel no
    else if (tel.length > 0 && !is_valid_Tel(tel)) {
        alert("Invalid telephone number!");
    }
    // check for valid letters
    else if (name.length > 0 && !is_valid_letter(name)) {
        alert("Invalid letters for name!");
    }
    // no error
    else {
        return false;
    }
    return true;
}
