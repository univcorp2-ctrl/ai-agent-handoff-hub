--!strict

local Csv = {}

local HEADERS = {
	"path",
	"class_name",
	"name",
	"text",
	"text_length",
	"auto_localize",
	"localization_match_identifier",
	"warnings",
}

local function escape(value: any): string
	local text = if value == nil then "" else tostring(value)
	local mustQuote = string.find(text, ",", 1, true)
		or string.find(text, '"', 1, true)
		or string.find(text, "\r", 1, true)
		or string.find(text, "\n", 1, true)

	if string.find(text, '"', 1, true) then
		text = string.gsub(text, '"', '""')
	end

	if mustQuote then
		return '"' .. text .. '"'
	end
	return text
end

function Csv.escape(value: any): string
	return escape(value)
end

function Csv.encode(findings: { any }): string
	local rows: { string } = {}
	table.insert(rows, table.concat(HEADERS, ","))

	for _, finding in findings do
		local warningText = ""
		if typeof(finding.warnings) == "table" then
			warningText = table.concat(finding.warnings, "|")
		end

		local row = {
		escape(finding.path),
		escape(finding.className),
		escape(finding.name),
		escape(finding.text),
		escape(finding.textLength),
		escape(finding.autoLocalize),
		escape(finding.localizationMatchIdentifier),
		escape(warningText),
		}
		table.insert(rows, table.concat(row, ","))
	end

	return table.concat(rows, "\r\n")
end

return Csv
