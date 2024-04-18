// declaring lightMode variable and retreiving value from local storage
let lightMode = localStorage.getItem("lightMode")

// Default classes to display
let classes = [
    {
        name: "447",
        canvasID: "123",
        recitations: ["10a", "12p"]
    },
    {
        name: "449",
        canvasID: "456",
        recitations: ["11a", "1p"]
    }
]

// Default channels to display
let template = [
    {
        channelName: "Announcements",
        channelType: "A",
        studentOnly: true,
        taOnly: true
    },
    {
        channelName: "qa-forum",
        channelType: "F",
        studentOnly: true,
        taOnly: false
    },
    {
        channelName: "general",
        channelType: "T",
        studentOnly: true,
        taOnly: false
    },
    {
        channelName: "assignment-discussion",
        channelType: "V",
        studentOnly: true,
        taOnly: false
    },
    {
        channelName: "ta-chat",
        channelType: "T",
        studentOnly: true,
        taOnly: true
    }
]

// return the integer index of the item you selected in the selection box
function get_selected_child_index(element) {
    for(let i = 0; i < element.children.length; i++) {
        if (element.children[i].selected) {
            return i
        }
    }
}

// boolean function, returns true if the object is an event
function is_event(obj) {
    return Event.prototype.isPrototypeOf(obj)
}

// no return, updating the fields for classes
function update_class_ui() {
    // Get selected class
    const classes_elem = document.getElementById('classes')
    const selected_child_index = get_selected_child_index(classes_elem)
    const selected_child = classes_elem.children.item(selected_child_index)

    // Get the text input elements
    const name_elem = document.getElementById('className')
    const canvas_id_elem = document.getElementById('classCanvasID')
    const recitation_time_elem = document.getElementById('recitationTime')

    // Set the text elements to what we want
    name_elem.value = selected_child.innerText
    canvas_id_elem.value = selected_child.dataset.canvasID
    recitation_time_elem.value = ""

    // Prepare to reset the recitations list
    const recitations_elem = document.getElementById('recitations')
    const recitations = JSON.parse(selected_child.dataset.recitations)

    // Empty recitations list
    for(let i = recitations_elem.childElementCount; i > 0; i--) {
        recitations_elem.removeChild(recitations_elem.firstElementChild)
    }

    // Re-fill recitations list (and select the first item if it exists) using data from selected class
    for(let rec of recitations) {
        add_new_recitation(rec)
    }
    if(recitations_elem.children.length) {
        recitations_elem.firstElementChild.selected = true
        update_recitation_ui()
    }
}

// no return, updating the fields for recitations
function update_recitation_ui() {
    const recitations_elem = document.getElementById('recitations')
    const recitation_time_elem = document.getElementById('recitationTime')

    // If we have no recitations return
    if(!recitations_elem.children.length) {
        recitation_time_elem.value = ""
        return
    }

    // Fill the text box
    const selected_child_index = get_selected_child_index(recitations_elem)
    const selected_child = recitations_elem.children.item(selected_child_index)
    recitation_time_elem.value = selected_child.innerText
}

// no return, removing a recitation from the config and calling update_ui()
function remove_recitation() {
    const recitations_elem = document.getElementById('recitations')
    const selected_index = get_selected_child_index(recitations_elem)
    const selected = recitations_elem.children.item(selected_index)

    // because we're storing data in the html element this is actually all we need to do
    recitations_elem.removeChild(selected)
    // it might conceivably be more efficient to only save the changed item (recitations) but I'm not worried
    update_course()

    // make sure the UI stays nice
    if(recitations_elem.firstElementChild) {
        recitations_elem.firstElementChild.selected = true
        update_recitation_ui()
    } else {
        document.getElementById('recitationTime').value = ""
    }
}

// no return, adding a new course to the config and calling update_ui()
function add_new_course(new_course) {
    // if this is used as an event handler (it is) then the first argument that gets passed in is the event
    if(!new_course || is_event(new_course)) {
        new_course = {
            name: "new course",
            canvasID: "0",
            recitations: []
        }
    }

    // create the new element and set ts data according to what was passed in
    const new_course_elem = document.createElement('option')
    new_course_elem.innerText = new_course.name
    new_course_elem.dataset.canvasID = new_course.canvasID
    new_course_elem.dataset.recitations = JSON.stringify(new_course.recitations)

    // add it to the UI and selected it (nice UI feature when you click the button)
    document.getElementById('classes').appendChild(new_course_elem)
    new_course_elem.selected = true
    update_class_ui()
}

// no return, adding a new recitation to the config and calling update_ui()
function add_new_recitation(new_rec) {
    // same as above, prevents trying to parse an event as the argument
    if(!new_rec || is_event(new_rec)) {
        new_rec = "8am"
    }

    // create the element and set its data
    const new_rec_elem = document.createElement('option')
    new_rec_elem.innerText = new_rec

    // add the new recitation to the list
    const recs_elem = document.getElementById('recitations')
    if(recs_elem.children.length > 9) {
        alert("Can't have more than 10 recitations!")
        return
    }
    recs_elem.appendChild(new_rec_elem)

    // Save the newly added recitation
    update_course()

    // UI niceties
    new_rec_elem.selected = true
    update_recitation_ui()
}

// no return, removing a course from the config and calling update_ui()
function remove_course () {
    const classes_elem = document.getElementById('classes')
    let selected_index = get_selected_child_index(classes_elem)
    const selected = classes_elem.children.item(selected_index)

    // Don't let the user remove all courses since I don't see a reason to allow that
    // Also means we don't have to handle the special case of not having anything in our options list
    if(classes_elem.children.length === 1) {
        alert("Cannot remove last course")
        return
    }

    // Again, the html is our data storage so this is sufficient
    classes_elem.removeChild(selected)

    // select the item that was above that one in the list (below if top) and update the UI accordingly
    if(selected_index > 0) selected_index -= 1
    classes_elem.children.item(selected_index).selected = true
    update_class_ui()
}

// update a course in the UI
function update_course() {
    // This saves the data elsewhere in the UI to our storage (the option element)
    const class_name_elem = document.getElementById('className')
    const class_id_elem = document.getElementById('classCanvasID')
    const classes_elem = document.getElementById('classes')

    const selected_index = get_selected_child_index(classes_elem)
    const selected = classes_elem.children.item(selected_index)

    const recitations_elem = document.getElementById('recitations')
    let recs = []
    for(let child of recitations_elem.children) {
        recs.push(child.innerText)
    }

    selected.innerText = class_name_elem.value
    selected.dataset.canvasID = class_id_elem.value
    selected.dataset.recitations = JSON.stringify(recs)
}

// update a recitation in the UI
function update_rec() {
    const rec_time_elem = document.getElementById('recitationTime')
    const recs_elem = document.getElementById('recitations')
    const selected_index = get_selected_child_index(recs_elem)
    const selected = recs_elem.children.item(selected_index)

    selected.innerText = rec_time_elem.value
}

/* BEGIN TEMPLATE MANAGEMENT CODE */

// save a channel into the config
function save_channel() {
    const channels_elem = document.getElementById('classTemplate')
    const selected_index = get_selected_child_index(channels_elem)
    const selected = channels_elem.children.item(selected_index)
    const template_form = document.getElementById('templateConfig')

    selected.innerText = template_form.elements.channelName.value
    selected.dataset.channelType = template_form.elements.channelType.value
    selected.dataset.studentOnly = JSON.stringify(template_form.elements.studentOnly.checked)
    selected.dataset.taOnly = JSON.stringify(template_form.elements.taOnly.checked)
}

// load a channel into the ui
function load_channel() {
    const channels_elem = document.getElementById('classTemplate')
    const selected_index = get_selected_child_index(channels_elem)
    const selected = channels_elem.children.item(selected_index)
    const form_elem = document.getElementById('templateConfig')

    form_elem.elements.channelName.value = selected.innerText
    form_elem.elements.channelType.value = selected.dataset.channelType
    form_elem.elements.studentOnly.checked = JSON.parse(selected.dataset.studentOnly)
    form_elem.elements.taOnly.checked = JSON.parse(selected.dataset.taOnly)
}

// add a channel into the config and have it be seen in the ui
function add_new_channel(new_channel) {
    if(!new_channel || is_event(new_channel)) {
        new_channel = {
            channelName: "New Channel",
            channelType: "T",
            studentOnly: true,
            taOnly: false
        }
    }
    const channels_elem = document.getElementById('classTemplate')
    const new_channel_elem = document.createElement('option')
    new_channel_elem.innerText = new_channel.channelName
    new_channel_elem.dataset.channelType = new_channel.channelType
    new_channel_elem.dataset.studentOnly = new_channel.studentOnly
    new_channel_elem.dataset.taOnly = new_channel.taOnly

    channels_elem.appendChild(new_channel_elem)
}

// remove a channel from the config and from being seen in the ui
function remove_channel() {
    const channels_elem = document.getElementById('classTemplate')
    let selected_index = get_selected_child_index(channels_elem)
    const selected = channels_elem.children.item(selected_index)

    if(channels_elem.children.length < 2) {
        alert("Can't remove last channel in template")
        return
    }
    channels_elem.removeChild(selected)
    if(selected_index > 0) selected_index -= 1
    channels_elem.children.item(selected_index).selected = true
    load_channel()
}

/* END TEMPLATE MANAGEMENT CODE */

//send the config to the Discord bot
function send_config() {
    const courses_elem = document.getElementById('classes')
    const template_elem = document.getElementById('classTemplate')

    let config_classes = []
    for(let child of courses_elem.children) {
        let this_class = {
            name: child.innerText,
            canvasID: child.dataset.canvasID,
            recitations: JSON.parse(child.dataset.recitations)
        }
        config_classes.push(this_class)
    }

    let config_template = []
    for(let child of template_elem.children) {
        let this_chan = {
            channelName: child.innerText,
            channelType: child.dataset.channelType,
            studentOnly: JSON.parse(child.dataset.studentOnly),
            taOnly: JSON.parse(child.dataset.taOnly)
        }
        config_template.push(this_chan)
    }

    const config = {
        template: config_template,
        classes: config_classes
    }

    console.log("Config to be sent:")
    console.log(config)

    let headers = new Headers()
    headers.append('Content-type', 'application/json')

    let fetch_options = {
        headers: headers,
        method: "POST",
        body: JSON.stringify(config)
    }

    showWaitDialog('Sending config to the bot! Please wait...')

    fetch("/config", fetch_options)
        .then((response) => {
            return response.json()
        })
        .then((response) => {
            if(response[0] === 0) {
                get_current_json()
                showFinishedDialog('Successfully configured semester channels and roles!')
            } else {
                showFinishedDialog('Something went wrong during the process! Sorry! Try the semester cleanup option, and manually delete what remains. Then, try again.')
            }
        })
        .catch((err) => {
            console.log(err)
            showFinishedDialog('Something went wrong! Please check the javascript console for more.')
        })
}

//get the json from the server and inputting it into the left div
function get_current_json() {
    fetch("/get_server_json")
        .then((response) => {
            if(response.status === 200) {
                return response.json()
            } else {
                throw new Error('Getting server JSON failed!')
            }
        })
        .then((response) => {
            document.getElementById('serverPanel').style.opacity = "1"
            fill_out_server_panel(response)
            console.log("Successfully loaded server layout")
        })
        .catch((err) => {
            document.getElementById('serverPanel').style.opacity = "0.5"
            console.log(err)
        })
}

// send semester cleanup to bot, freeze interaction for UI, and display informative popups to user
function send_semester_cleanup() {
    if (prompt('Are you sure you want to ERASE all managed categories, and migrate current students and TAs to former-student roles?\nType "YES" to confirm!') === "YES") {
        showWaitDialog('Sending cleanup request! Please wait...')
        const fetch_options = {
            method: "DELETE"
        }
        fetch("/cleanup", fetch_options)
            .then((response) => {
                return response.json()
            })
            .then((response) => {
                if(response[0] === 0) {
                    get_current_json()
                    showFinishedDialog('Successfully cleaned up!')
                } else {
                    showFinishedDialog('Something went wrong during the process! Sorry! You may need to manually delete channels and migrate students.')
                }
            })
            .catch((error) => {
                console.log(error)
                showFinishedDialog('Some error occurred! Check the javascript console for more information')
            })
    } else {
        showFinishedDialog("You didn't type YES, cleanup not performed")
    }
}

// fill in top div with channel information
function fill_out_server_panel(config) {
    let server_elem = document.getElementById('server')
    while(server_elem.hasChildNodes()) {
        server_elem.removeChild(server_elem.firstChild)
    }
    for(let entry of config) {
        if(entry.channels) {
            const grp_elem = document.createElement('optgroup')
            grp_elem.label = entry.name
            if(entry.managed) {
                grp_elem.classList.add('managed')
            }
            for(let chan of entry.channels) {
                const chan_elem = document.createElement('option')
                chan_elem.innerText = chan.name
                grp_elem.appendChild(chan_elem)
            }
            server_elem.appendChild(grp_elem)
        } else {
            const chan_elem = document.createElement('option')
            chan_elem.innerText = entry.name
            server_elem.appendChild(chan_elem)
        }
    }
}

// show the wait pop up while the user is waiting
function showWaitDialog(string = 'Processing! Please wait...') {
    document.getElementById('waitDialogText').innerText = string
    document.getElementById('waitDialog').showModal()
}

// show the finished pop up once the user is done waiting
function showFinishedDialog(string = "Finished!") {
    document.getElementById('finishedDialogText').innerText = string
    document.getElementById('finishedDialog').showModal()
    document.getElementById('finishedDialogBtn').focus()
}

// close the notices that pop up when waiting
function closeDialogs() {
    document.getElementById('finishedDialog').close()
    document.getElementById('waitDialog').close()
}

// no return, change the colors of the ui - from a darker color pallete, to a lighter color pallete (or reverse)
function changeMode() {
    lightMode = localStorage.getItem('lightMode')

    if (lightMode === 'enabled') {
        enableDark()
    } else {
        enableLight()
    }
}

// helper function for changeMode(), changing the colors to light ones and storing in local sorage
function enableLight() {
    document.body.classList.add('lightMode')
    localStorage.setItem('lightMode', 'enabled')
}

// helper function for changeMode(), changing the colors to dark ones and storing in local sorage
function enableDark() {
    document.body.classList.remove('lightMode')
    localStorage.setItem('lightMode', null)
}

// once content has been loaded, make all buttons and entry fields active
function onload() {
    // document.body.classList.add('lightMode');
    for(let chan of template) {
        add_new_channel(chan)
    }

    const template_elem = document.getElementById('classTemplate')
    template_elem.firstElementChild.selected = true
    load_channel()
    template_elem.addEventListener('change', load_channel)
    document.getElementById('templateConfig').addEventListener('input', save_channel)
    document.getElementById('rmChanBtn').addEventListener('click', remove_channel)
    document.getElementById('addChanBtn').addEventListener('click', add_new_channel)

    for(let sem_class of classes) {
        add_new_course(sem_class)
    }

    const classes_elem = document.getElementById("classes")
    classes_elem.firstElementChild.selected = true
    update_class_ui()

    classes_elem.addEventListener("change", update_class_ui)

    document.getElementById('addClassBtn').addEventListener("click", add_new_course)
    document.getElementById('removeClassBtn').addEventListener("click", remove_course)

    document.getElementById('className').addEventListener('input', update_course)
    document.getElementById('classCanvasID').addEventListener('change', update_course)

    document.getElementById('recitations').addEventListener("change", update_recitation_ui)

    document.getElementById('rmRecBtn').addEventListener('click', remove_recitation)
    document.getElementById('addRecBtn').addEventListener('click', add_new_recitation)

    const rec_time_elem = document.getElementById('recitationTime')
    rec_time_elem.addEventListener('input', update_rec)
    rec_time_elem.addEventListener('change', update_course)

    document.getElementById('semCommitBtn').addEventListener('click', send_config)
    document.getElementById('semCleanupBtn').addEventListener('click', send_semester_cleanup)

    document.getElementById('finishedDialogBtn').addEventListener('click', closeDialogs)

    document.getElementById('modeBtn').addEventListener('click', changeMode)
    
    if (lightMode === "enabled") enableLight()

    get_current_json()
}

addEventListener("DOMContentLoaded", onload)
