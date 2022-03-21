Back to [All Modules](https://github.com/pyrustic/litemark/blob/master/docs/modules/README.md#readme)

# Module Overview

**litemark.core.viewer**
 
No description

> **Classes:** &nbsp; [Error](https://github.com/pyrustic/litemark/blob/master/docs/modules/content/litemark.core.viewer/content/classes/Error.md#class-error) &nbsp;&nbsp; [Info](https://github.com/pyrustic/litemark/blob/master/docs/modules/content/litemark.core.viewer/content/classes/Info.md#class-info) &nbsp;&nbsp; [TokenError](https://github.com/pyrustic/litemark/blob/master/docs/modules/content/litemark.core.viewer/content/classes/TokenError.md#class-tokenerror) &nbsp;&nbsp; [Viewer](https://github.com/pyrustic/litemark/blob/master/docs/modules/content/litemark.core.viewer/content/classes/Viewer.md#class-viewer) &nbsp;&nbsp; [WidgetError](https://github.com/pyrustic/litemark/blob/master/docs/modules/content/litemark.core.viewer/content/classes/WidgetError.md#class-widgeterror)
>
> **Functions:** &nbsp; [button\_press\_effect](https://github.com/pyrustic/litemark/blob/master/docs/modules/content/litemark.core.viewer/content/functions.md#button_press_effect) &nbsp;&nbsp; [button\_release\_effect](https://github.com/pyrustic/litemark/blob/master/docs/modules/content/litemark.core.viewer/content/functions.md#button_release_effect) &nbsp;&nbsp; [define\_tags](https://github.com/pyrustic/litemark/blob/master/docs/modules/content/litemark.core.viewer/content/functions.md#define_tags) &nbsp;&nbsp; [free\_images\_cache](https://github.com/pyrustic/litemark/blob/master/docs/modules/content/litemark.core.viewer/content/functions.md#free_images_cache) &nbsp;&nbsp; [get\_dark\_style](https://github.com/pyrustic/litemark/blob/master/docs/modules/content/litemark.core.viewer/content/functions.md#get_dark_style) &nbsp;&nbsp; [get\_light\_style](https://github.com/pyrustic/litemark/blob/master/docs/modules/content/litemark.core.viewer/content/functions.md#get_light_style) &nbsp;&nbsp; [insert\_codeblock](https://github.com/pyrustic/litemark/blob/master/docs/modules/content/litemark.core.viewer/content/functions.md#insert_codeblock) &nbsp;&nbsp; [insert\_image](https://github.com/pyrustic/litemark/blob/master/docs/modules/content/litemark.core.viewer/content/functions.md#insert_image) &nbsp;&nbsp; [insert\_inlink](https://github.com/pyrustic/litemark/blob/master/docs/modules/content/litemark.core.viewer/content/functions.md#insert_inlink) &nbsp;&nbsp; [insert\_link](https://github.com/pyrustic/litemark/blob/master/docs/modules/content/litemark.core.viewer/content/functions.md#insert_link) &nbsp;&nbsp; [on\_button\_press\_1\_link](https://github.com/pyrustic/litemark/blob/master/docs/modules/content/litemark.core.viewer/content/functions.md#on_button_press_1_link) &nbsp;&nbsp; [on\_button\_press\_3\_codeblock](https://github.com/pyrustic/litemark/blob/master/docs/modules/content/litemark.core.viewer/content/functions.md#on_button_press_3_codeblock) &nbsp;&nbsp; [on\_button\_press\_3\_link](https://github.com/pyrustic/litemark/blob/master/docs/modules/content/litemark.core.viewer/content/functions.md#on_button_press_3_link) &nbsp;&nbsp; [on\_button\_release\_1\_inlink](https://github.com/pyrustic/litemark/blob/master/docs/modules/content/litemark.core.viewer/content/functions.md#on_button_release_1_inlink) &nbsp;&nbsp; [on\_button\_release\_1\_link](https://github.com/pyrustic/litemark/blob/master/docs/modules/content/litemark.core.viewer/content/functions.md#on_button_release_1_link) &nbsp;&nbsp; [on\_button\_release\_3\_codeblock](https://github.com/pyrustic/litemark/blob/master/docs/modules/content/litemark.core.viewer/content/functions.md#on_button_release_3_codeblock) &nbsp;&nbsp; [on\_button\_release\_3\_link](https://github.com/pyrustic/litemark/blob/master/docs/modules/content/litemark.core.viewer/content/functions.md#on_button_release_3_link) &nbsp;&nbsp; [on\_enter\_codeblock](https://github.com/pyrustic/litemark/blob/master/docs/modules/content/litemark.core.viewer/content/functions.md#on_enter_codeblock) &nbsp;&nbsp; [on\_enter\_link](https://github.com/pyrustic/litemark/blob/master/docs/modules/content/litemark.core.viewer/content/functions.md#on_enter_link) &nbsp;&nbsp; [on\_leave\_codeblock](https://github.com/pyrustic/litemark/blob/master/docs/modules/content/litemark.core.viewer/content/functions.md#on_leave_codeblock) &nbsp;&nbsp; [on\_leave\_link](https://github.com/pyrustic/litemark/blob/master/docs/modules/content/litemark.core.viewer/content/functions.md#on_leave_link) &nbsp;&nbsp; [open\_website](https://github.com/pyrustic/litemark/blob/master/docs/modules/content/litemark.core.viewer/content/functions.md#open_website) &nbsp;&nbsp; [remove\_empty\_lines](https://github.com/pyrustic/litemark/blob/master/docs/modules/content/litemark.core.viewer/content/functions.md#remove_empty_lines) &nbsp;&nbsp; [render](https://github.com/pyrustic/litemark/blob/master/docs/modules/content/litemark.core.viewer/content/functions.md#render) &nbsp;&nbsp; [setup\_style](https://github.com/pyrustic/litemark/blob/master/docs/modules/content/litemark.core.viewer/content/functions.md#setup_style) &nbsp;&nbsp; [update\_clipboard](https://github.com/pyrustic/litemark/blob/master/docs/modules/content/litemark.core.viewer/content/functions.md#update_clipboard)
>
> **Constants:** &nbsp; IMAGES_CACHE

# Class Viewer
No description.

## Base Classes
object

## Class Attributes


## Class Properties
|Property|Type|Description|Inherited from|
|---|---|---|---|
|readonly|getter|None||
|readonly|setter|None||
|root|getter|None||
|style|getter|None||
|tokens|getter|None||
|widget|getter|None||



# All Methods
[\_\_init\_\_](#__init__) &nbsp;&nbsp; [\_setup](#_setup) &nbsp;&nbsp; [anchor](#anchor) &nbsp;&nbsp; [clear](#clear) &nbsp;&nbsp; [open](#open) &nbsp;&nbsp; [render](#render)

## \_\_init\_\_
Initialize self.  See help(type(self)) for accurate signature.



**Signature:** (self, widget=None, root=None, style=<litemark.core.style.Style object at 0x7fbf554c3e20>, on\_browse=None)





**Return Value:** None.

[Back to Top](#module-overview)


## \_setup
None



**Signature:** (self)





**Return Value:** None.

[Back to Top](#module-overview)


## anchor
name = heading



**Signature:** (self, name)





**Return Value:** None.

[Back to Top](#module-overview)


## clear
None



**Signature:** (self)





**Return Value:** None.

[Back to Top](#module-overview)


## open
None



**Signature:** (self, path)





**Return Value:** None.

[Back to Top](#module-overview)


## render
data = string or tokens



**Signature:** (self, data)





**Return Value:** None.

[Back to Top](#module-overview)



