// File Name:     virtual_keyboard.js
// By:            Darian Benam (GitHub: https://github.com/BeardedFish/)
// Date:          Wednesday, May 6, 2020

var virtualKeyboardCapsLockOn = false;
var virtualKeyboardShiftOn = false;
var isSending = false;

function sendDataToServer() {
    var text = $("#write-area").val();
    if (text.trim() === "" || isSending) return;

    isSending = true;

    $.ajax({
        url: '/api/input',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ input_text: text }),

        beforeSend: function() {
            $("#loader").removeClass("done");
        },
        success: function(response) {
            if (response.hint_words && response.hint_words.length > 0) {
                const hintsHtml = response.hint_words
                    .map(word => `<div class="hint-key">${word}</div>`)
                    .join("");
                $("#hint-words").html(hintsHtml);
            } else {
                $("#hint-words").html("<em>Нет подсказок</em>");
            }
        },
        complete: function() {
            $("#loader").addClass("done");
            isSending = false;
        }
    });
}


$.fn.selectRange = function(start, end) // Function borrowed from: https://stackoverflow.com/a/841121/11760346/
{
    if (end === undefined)
    {
        end = start;
    }

    return this.each(function()
    {
        if("selectionStart" in this)
        {
            this.selectionStart = start;
            this.selectionEnd = end;
        }
        else if (this.setSelectionRange)
        {
            this.setSelectionRange(start, end);
        }
        else if (this.createTextRange)
        {
            var range = this.createTextRange();
            range.collapse(true);
            range.moveEnd("character", end);
            range.moveStart("character", start);
            range.select();
        }
    });
};

$(function()
{
    $("#write-area").on("keydown", function(e) {
        if (e.key === "Enter") {
            e.preventDefault();
            if (!isSending) {
                sendDataToServer();
            }
        }
    });
    // Regular letters (a, b, c, etc.)
    $("#virtual-keyboard .regular-key").click(function()
    {
        var character = $(this).find("span").html(); // The actual key that was clicked on the virtual keyboard

        if ($(this).hasClass("uppercase"))
        {
            character = character.toUpperCase();
        }

        insertAtCaret(document.getElementById("write-area"), character);
        translit(this);
    });

    // Symbol characters (!, @, #, etc.)
    $("#virtual-keyboard .symbol-key").click(function()
    {
        var character = $("span:visible", $(this)).html(); // Get the visible span inner text

        if (character === "&amp;") // Convert HTML ampersand code to the ampersand sign
        {
            character = '&';
        }

        insertAtCaret(document.getElementById("write-area"), character);
        translit(this);
    });

    // Special keys (backspace, shift, tab, etc.)
    $("#virtual-keyboard .special-key").click(function()
    {
        var specialKey = $(this).find("span").html(); // The actual key that was clicked on the virtual keyboard

        if (specialKey === "Backspace")
        {
            var startPos = document.getElementById("write-area").selectionStart;
            var endPos = document.getElementById("write-area").selectionEnd;

            if (endPos == 0) // There is nothing to backspace
            {
                return;
            }

            var text = $("#write-area").val();
            var offset = startPos == endPos ? 1 : 0;
            var newText = text.substring(0, startPos - offset) + text.substring(endPos);
            
            $("#write-area").val(newText);
            $("#write-area").focus();
            $("#write-area").selectRange(startPos - offset);  

            return;
        }
        else if (specialKey === "Caps Lock")
        {
            $(this).toggleClass("special-key-on");
            $(".regular-key").toggleClass("uppercase");

            virtualKeyboardCapsLockOn = $(this).hasClass("special-key-on");

            if (!virtualKeyboardShiftOn)
            {
                toggleKeysUppercase();
            }

            return;
        }
        else if (specialKey === "Enter")
        {
            sendDataToServer();
            return;
        }
        else if (specialKey === "Shift")
        {
            $("#left-shift").toggleClass("special-key-on");
            $("#right-shift").toggleClass("special-key-on");
        
            $(".regular-key").toggleClass("uppercase");
            $(".symbol-key span").toggle();
            
            if (!virtualKeyboardCapsLockOn)
            {
                toggleKeysUppercase();
            }
        
            virtualKeyboardShiftOn = !virtualKeyboardShiftOn;
            
            return;
        }
        else if (specialKey === "Space")
        {
            specialKey = " ";
        }
        else if (specialKey === "Tab")
        {
            specialKey = "\t";
        }

        insertAtCaret(document.getElementById("write-area"), specialKey);

    });
    $(document).on("click", ".hint-key", function(e) {
        e.preventDefault();
        var word = $(this).text().trim();
        if (!word) return;

        var textarea = document.getElementById("write-area");

        var needLeadingSpace = textarea.selectionStart === textarea.value.length && textarea.value.length > 0 && !textarea.value.endsWith(" ");
        var toInsert = (needLeadingSpace ? " " : "") + word;

        insertAtCaret(textarea, toInsert);
        $("#write-area").focus();
        console.log("hint-key inserted:", word);
    });
});

function insertAtCaret(element, text)
{
    if (document.selection)
    {
        element.focus();  

        var sel = document.selection.createRange();
        sel.text = text;

        element.focus();
    }
    else if (element.selectionStart || element.selectionStart === 0)
    {
        var startPos = element.selectionStart;
        var endPos = element.selectionEnd;
        var scrollTop = element.scrollTop;

        element.value = element.value.substring(0, startPos) + text + element.value.substring(endPos, element.value.length);

        element.focus();

        element.selectionStart = startPos + text.length;
        element.selectionEnd = startPos + text.length;
        element.scrollTop = scrollTop;
    }
    else
    {
        element.value += text;

        element.focus();
    }
}

function toggleKeysUppercase()
{
    $(".keyboard-row").find("div").each(function()
    {
        if ($(this).hasClass("regular-key"))
        {
            var newChar = $(this).hasClass("uppercase") ? $(this).html().toUpperCase() : $(this).html().toLowerCase();
            $(this).html(newChar);
        }
    });
}