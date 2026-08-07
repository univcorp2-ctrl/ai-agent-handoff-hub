--!strict

-- Pure Luau behavior specification. The implementation agent should wire this
-- into the selected current test runner after verifying the toolchain.

local Csv = require(script.Parent.Parent.src.csv)

local function assertEqual(actual: any, expected: any, label: string)
	if actual ~= expected then
		error(string.format("%s: expected %q, got %q", label, tostring(expected), tostring(actual)))
	end
end

assertEqual(Csv.escape("plain"), "plain", "plain text")
assertEqual(Csv.escape("a,b"), '"a,b"', "comma")
assertEqual(Csv.escape('say "hi"'), '"say ""hi"""', "double quote")
assertEqual(Csv.escape("line1\nline2"), '"line1\nline2"', "newline")
assertEqual(Csv.escape("日本語"), "日本語", "unicode")
assertEqual(Csv.escape(nil), "", "nil")

local encoded = Csv.encode({
	{
		path = "game.ScreenGui.Label",
		className = "TextLabel",
		name = "Label",
		text = "こんにちは, 世界",
		textLength = 8,
		autoLocalize = false,
		localizationMatchIdentifier = "",
		warnings = { "AUTOLOCALIZE_DISABLED", "HARD_CODED_TEXT_CANDIDATE" },
	},
})

if not string.find(encoded, '"こんにちは, 世界"', 1, true) then
	error("encoded CSV did not quote Japanese text containing a comma")
end
if not string.find(encoded, "AUTOLOCALIZE_DISABLED|HARD_CODED_TEXT_CANDIDATE", 1, true) then
	error("encoded CSV did not join warning codes")
end

print("csv.spec.lua: PASS")
