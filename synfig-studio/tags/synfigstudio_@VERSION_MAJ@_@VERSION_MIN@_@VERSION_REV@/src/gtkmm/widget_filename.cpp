/* === S Y N F I G ========================================================= */
/*!	\file widget_filename.cpp
**	\brief Template File
**
**	$Id$
**
**	\legal
**	Copyright (c) 2002-2005 Robert B. Quattlebaum Jr., Adrian Bentley
**	Copyright (c) 2008 Chris Moore
**
**	This package is free software; you can redistribute it and/or
**	modify it under the terms of the GNU General Public License as
**	published by the Free Software Foundation; either version 2 of
**	the License, or (at your option) any later version.
**
**	This package is distributed in the hope that it will be useful,
**	but WITHOUT ANY WARRANTY; without even the implied warranty of
**	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
**	General Public License for more details.
**	\endlegal
*/
/* ========================================================================= */

/* === H E A D E R S ======================================================= */

#ifdef USING_PCH
#	include "pch.h"
#else
#ifdef HAVE_CONFIG_H
#	include <config.h>
#endif

#include <gtkmm/entry.h>
#include <gtkmm/button.h>
#include "widget_filename.h"
#include "app.h"
#include "canvasview.h"

#include "general.h"

#endif

/* === U S I N G =========================================================== */

using namespace std;
//using namespace etl;
//using namespace synfig;
using namespace studio;

/* === M A C R O S ========================================================= */

/* === G L O B A L S ======================================================= */

/* === P R O C E D U R E S ================================================= */

/* === M E T H O D S ======================================================= */

Widget_Filename::Widget_Filename()
{
	entry_filename=manage(new Gtk::Entry());
	button_choose=manage(new Gtk::Button(_("Find")));

	pack_start(*entry_filename);
	pack_start(*button_choose);
	entry_filename->show();
	button_choose->show();

	button_choose->signal_clicked().connect(sigc::mem_fun(*this, &studio::Widget_Filename::on_button_choose_pressed));
	//entry_filename->signal_value_changed().connect(sigc::mem_fun(*this, &studio::Widget_Filename::on_value_changed));
	entry_filename->signal_activate().connect(sigc::mem_fun(*this, &studio::Widget_Filename::on_value_changed));
}

Widget_Filename::~Widget_Filename()
{
}

void
Widget_Filename::set_has_frame(bool x)
{
	entry_filename->set_has_frame(x);
}


void
Widget_Filename::set_value(const std::string &data)
{
	entry_filename->set_text(data);
}

string
Widget_Filename::get_value() const
{
	try
	{
		return entry_filename->get_text();
	}
	catch(...)
	{
		throw string("Caught unknown exception");
	}
}

void
Widget_Filename::on_value_changed()
{
	signal_value_changed()();
}

void
Widget_Filename::on_button_choose_pressed()
{
	string filename=entry_filename->get_text();
	if(filename.empty())
		filename=".";
	else
		filename = etl::absolute_path(
			etl::dirname(App::get_selected_canvas_view()->get_canvas()->get_file_name()) +
			ETL_DIRECTORY_SEPARATOR +
			filename);
	if(App::dialog_open_file(_("Choose File"), filename, MISC_DIR_PREFERENCE))
		entry_filename->set_text(filename);
}
