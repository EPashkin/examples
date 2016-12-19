//! # Basic Sample
//!
//! This sample demonstrates how to create a toplevel `window`, set its title, size and position, how to add a `button` to this `window` and how to connect signals with actions.

#![crate_type = "bin"]

extern crate glib;
extern crate gtk;
extern crate gdk_pixbuf;

use gtk::prelude::*;
use gtk::{
    Assistant, AssistantPageType, Box as Box_, ButtonsType, Entry, Label, MessageDialog, MessageType, Orientation, DIALOG_MODAL,
};
use gdk_pixbuf::Pixbuf;

fn main() {
    if gtk::init().is_err() {
        println!("Failed to initialize GTK.");
        return;
    }

    let assistant = Assistant::new();
    assistant.set_size_request(450, 300);
    assistant.set_title("GtkAssistant Example");

    let page1 = Label::new(Some(r#"This is an example of a GtkAssistant. By
clicking the forward button, you can continue
to the next section!"#));
    assistant.append_page(&page1);
    assistant.set_page_title(&page1, "page1 title");
    assert_eq!("page1 title", assistant.get_page_title(&page1).unwrap());
    assistant.set_page_type(&page1, AssistantPageType::Intro);
    println!("{:?}", assistant.get_page_type(&page1));
    assistant.set_page_complete(&page1, true);

    /*
    let image = Pixbuf::new_from_file("./resources/eye.png").or_else(|err| {
        let mut msg = err.to_string();
        if err.kind() == Some(glib::FileError::Noent) {
            msg.push_str(&format!("\nRelaunch this example from the same level \
                                  as the `resources` folder"));
        }
        let window = assistant.clone();

        gtk::idle_add(move || {
            let dialog = MessageDialog::new(Some(&window), DIALOG_MODAL,
                MessageType::Error, ButtonsType::Ok, &msg);
            dialog.run();
            dialog.destroy();
            Continue(false)
        });

        Err(())
    }).ok();
    assistant.set_child_sidebar_image(&page1, image.as_ref());
    assistant.set_child_header_image(&page1, image.as_ref());
    */

    let page2 = Box_::new(Orientation::Horizontal, 5);
    let label1 = Label::new(Some("Your Name: "));
    page2.pack_start(&label1, false, false, 5);
    let entry = Entry::new();
    page2.pack_start(&entry, false, false, 5);
    assistant.append_page(&page2);
    assistant.set_page_title(&page2, "page2 title");
    assistant.set_page_complete(&page2, true);

    assistant.connect_delete_event(|_, _| {
        gtk::main_quit();
        Inhibit(false)
    });

/*
    let window = gtk::Window::new(gtk::WindowType::Toplevel);

    window.set_border_width(10);
    window.set_position(gtk::WindowPosition::Center);
    window.set_default_size(350, 70);

    window.connect_delete_event(|_, _| {
        gtk::main_quit();
        Inhibit(false)
    });

    let button = gtk::Button::new_with_label("Click me!");

    window.add(&button);
*/
    assistant.show_all();
    gtk::main();
}