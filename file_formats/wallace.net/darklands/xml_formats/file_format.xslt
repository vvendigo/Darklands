<?xml version="1.0" encoding="UTF-8"?>
<xsl:transform version="1.0"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:fo="http://www.w3.org/1999/XSL/Format"
	xmlns:html="http://www.w3.org/1999/xhtml"
>

<xsl:output method="html" version="4.0"
	media-type="text/html"	encoding="iso-8859-1" indent="yes"
	doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN"
	doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"
/>

<!--
========== Global variables
-->

<xsl:variable name="gPathDelim">\</xsl:variable>
<xsl:variable name="gStyleSheet">file_format.css</xsl:variable>

<!-- ====================================================================== -->

<!--
========== Main document output
-->

<xsl:template match="/file">
<html>
<head>
	<title>
		File Format: <xsl:value-of select="@name" />
	</title>
	<link rel="stylesheet" type="text/css" href="{$gStyleSheet}" title="File Format" />
</head>
<body>

<h1>
	<xsl:value-of select="@name" />
</h1>

<!-- File globs and the file description block -->
<xsl:apply-templates select="globs" />
<xsl:apply-templates select="description" />

<!-- Table of contents -->
<h1 class="toc">Table of Contents</h1>
<xsl:apply-templates select="offsets|structdefs|enumerations" mode="toc" />

<!-- Contents (offsets) -->
<xsl:apply-templates select="./offsets" />

<!-- Structure definitions -->
<xsl:apply-templates select="./structdefs" />

<!-- Enumerations -->
<xsl:apply-templates select="./enumerations" />

<!-- Debugging info: the "ignore" block is output as-is -->
<xsl:if test="./ignore">
	<hr />
	<h1>(ignore this)</h1>
	<pre>
	<xsl:apply-templates select="./ignore" />
	</pre>
</xsl:if>

</body>
</html>
</xsl:template> 

<!-- ====================================================================== -->

<!--
========== Table of Contents
-->

<!-- Offsets TOC (in file order) -->
<xsl:template match="offsets" mode="toc">
	<xsl:if test="offset">
		<h2 class="toc-category">Offsets</h2>
		<xsl:apply-templates select="offset" mode="toc" />
	</xsl:if>
</xsl:template>

<!-- Structure definitions TOC (sorted) -->
<xsl:template match="structdefs" mode="toc">
	<xsl:if test="structdef">
		<h2 class="toc-category">Structures</h2>
		<xsl:apply-templates select="structdef" mode="toc">
			<xsl:sort select="@type" />
		</xsl:apply-templates>
	</xsl:if>
</xsl:template>

<!-- Enumerations TOC (sorted) -->
<xsl:template match="enumerations" mode="toc">
	<xsl:if test="enumeration">
		<h2 class="toc-category">Enumerations</h2>
		<xsl:apply-templates select="enumeration" mode="toc">
			<xsl:sort select="@type" />
		</xsl:apply-templates>
	</xsl:if>
</xsl:template>

<xsl:template match="offset" mode="toc">
	<div class="toc-entry">
		<xsl:call-template name="link-to-definition">
			<xsl:with-param name="type" select="name()" />
			<xsl:with-param name="name" select="@start" />
			<xsl:with-param name="label">
				<!-- Describe as either "from X to Y" or "starting at X" -->
				<!-- TODO: this looks like a function... -->
				<xsl:choose>
					<xsl:when test="@end">
						<xsl:text>from </xsl:text>
						<xsl:value-of select="@start" />
						<xsl:text> to </xsl:text>
						<xsl:value-of select="@end" />
					</xsl:when>
					<xsl:otherwise>
						<xsl:text>starting at </xsl:text>
						<xsl:value-of select="@start" />
					</xsl:otherwise>
				</xsl:choose>
			</xsl:with-param>
		</xsl:call-template>
	</div>
</xsl:template>

<xsl:template match="structdef|enumeration" mode="toc">
	<div class="toc-entry">
		<xsl:call-template name="link-to-definition">
			<xsl:with-param name="type" select="name()" />
			<xsl:with-param name="name" select="@type" />
			<xsl:with-param name="label" select="@type" />
		</xsl:call-template>
	</div>
</xsl:template>

<!-- ====================================================================== -->

<!--
========== File globs
-->

<xsl:template match="globs">
	<p>
		<xsl:text>Files with this format: </xsl:text>
		<xsl:apply-templates select="glob" />
		<xsl:text>.</xsl:text>
	</p>
</xsl:template>

<xsl:template match="glob">
	<xsl:text>"</xsl:text>
	<code>
		<!-- Prepend the directory (if any) -->
		<xsl:if test="@dir">
			<xsl:value-of select="@dir" />
			<xsl:value-of select="$gPathDelim" />
		</xsl:if>
		<xsl:value-of select="@filespec" />
	</code>
	<xsl:text>"</xsl:text>

	<!-- Separate from siblings by ';' -->
	<xsl:if test="following-sibling::*">
		<xsl:text>; </xsl:text>
	</xsl:if>
</xsl:template>

<!--
========== Contents (variables and structures at particular offsets)
-->

<xsl:template match="offsets">
	<hr />
	<h1>Offsets</h1>
	<xsl:apply-templates select="offset" />
</xsl:template>

<xsl:template match="offset">
	<!-- Section header and navigation anchor -->
	<h2>
		<a name="offset-{@start}">
			<xsl:text>Offset: </xsl:text>
			<!-- Describe as either "from X to Y" or "starting at X" -->
			<xsl:choose>
				<xsl:when test="@end">
					<xsl:text>from </xsl:text>
					<xsl:value-of select="@start" />
					<xsl:text> to </xsl:text>
					<xsl:value-of select="@end" />
				</xsl:when>
				<xsl:otherwise>
					<xsl:text>starting at </xsl:text>
					<xsl:value-of select="@start" />
				</xsl:otherwise>
			</xsl:choose>
		</a>
	</h2>

	<!-- The contents -->
	<dl>
		<xsl:apply-templates select="char|byte|word|dword|bit|int|string|struct|array|bitmask|unknown" />
	</dl>
</xsl:template>

<!--
========== Structure definitions
-->

<xsl:template match="structdefs">
	<xsl:if test="structdef">
		<hr />
		<h1>Structures</h1>
		<xsl:apply-templates select="structdef" />
	</xsl:if>
</xsl:template>

<xsl:template match="structdef">
	<!-- Section header and navigation anchor -->
	<h2>
		<a name="structdef-{@type}">
			<xsl:text>Structure: </xsl:text>
			<xsl:value-of select="@type" />
		</a>
	</h2>

	<!-- Size -->
	<xsl:if test="@size">
		<p>
			<xsl:text>Size </xsl:text>
			<xsl:value-of select="@size" />
			<xsl:text>.</xsl:text>
		</p>
	</xsl:if>

	<!-- Description and any notes -->
	<xsl:apply-templates select="./description" />
	<xsl:apply-templates select="./notes" />

	<!-- The structure -->
	<dl>
		<xsl:apply-templates select="char|byte|word|dword|bit|int|string|struct|array|bitmask|unknown" />
	</dl>
</xsl:template>

<!--
========== Enumerations
-->

<xsl:template match="enumerations">
	<xsl:if test="enumeration">
		<hr />
		<h1>Enumerations</h1>
		<xsl:apply-templates select="enumeration" />
	</xsl:if>
</xsl:template>

<xsl:template match="enumeration">
	<!-- Section header and navigation anchor -->
	<h2>
		<a name="enumeration-{@type}">
			<xsl:text>Enumeration: </xsl:text>
			<xsl:value-of select="@type" />
		</a>
	</h2>

	<!-- Description and any notes -->
	<xsl:apply-templates select="./description" />
	<xsl:apply-templates select="./notes" />

	<!-- The enumeration -->
	<table class="enum">
		<thead>
			<tr>
				<th class="enum-label">
					Data Value
				</th>
				<th class="enum-label">
					Meaning
				</th>
			</tr>
		</thead>
		<tbody>
			<xsl:apply-templates select="map" />
		</tbody>
	</table>
</xsl:template>

<xsl:template match="map">
	<tr>
		<td class="enum-value-from">
			<xsl:value-of select="@from" />
		</td>
		<td class="enum-value-to">
			<xsl:value-of select="@to" />
		</td>
	</tr>
</xsl:template>

<!--
========== Descriptions
-->

<!-- Descriptions default to 'paragraph', but might be more complex. -->
<xsl:template match="description">
	<xsl:choose>
		<xsl:when test="@type = 'extended'">
			<xsl:apply-templates select="." mode="extended" />
		</xsl:when>
		<xsl:when test="@type = 'simple'">
			<xsl:apply-templates select="." mode="simple" />
		</xsl:when>
		<xsl:otherwise>
			<xsl:apply-templates select="." mode="paragraph" />
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>

<!-- 'extended' descriptions are expected to contain their own block delimiters -->
<xsl:template match="description" mode="extended">
	<xsl:apply-templates select="html:*" />
</xsl:template>

<!-- 'paragraph' descriptions need a [p] block around them -->
<xsl:template match="description" mode="paragraph">
	<p>
		<xsl:apply-templates select="text() | html:*" />
	</p>
</xsl:template>

<!-- 'simple' descriptions are short and inline; a period must be appended -->
<xsl:template match="description" mode="simple">
	<xsl:apply-templates select="text() | html:*" />
</xsl:template>

<!--
========== Notes, and internal navigation links
-->

<xsl:template match="notes">
	<ul class="notes">
		<xsl:apply-templates select="note" />
	</ul>
</xsl:template>


<xsl:template match="note">
	<li class="note">
		<xsl:apply-templates select="text() | html:* | reference" />
	</li>
</xsl:template>

<xsl:template match="reference">
	<xsl:call-template name="link-to-definition">
		<xsl:with-param name="filename" select="@file" />
		<xsl:with-param name="type" select="@type" />
		<xsl:with-param name="name" select="@to" />
		<xsl:with-param name="label" select="." />
		<xsl:with-param name="add-optional-file-link" select="'yes'" />
	</xsl:call-template>
</xsl:template>

<!-- ====================================================================== -->

<!--
========== Variables (or structure members)
-->

<xsl:template match="char|byte|word|dword|bit|int|string|struct|array|bitmask|unknown">
	<dt>
		<span class="var-at">
			<xsl:apply-templates select="." mode="var-at" />
		</span>

		<span class="var-name">
			<xsl:apply-templates select="." mode="var-name" />
		</span>

		<xsl:if test="@unknown = 'yes'">
			<em>
			<xsl:text>unknown </xsl:text>
			</em>
		</xsl:if>

		<span class="var-datatype">
			<xsl:apply-templates select="." mode="var-datatype" />
		</span>

		<!-- Output details about the value and whether it is constant or not -->
		<xsl:choose>
			<xsl:when test="@constant = 'yes' and @value">
				<xsl:text> [constant: </xsl:text>
				<xsl:value-of select="@value" />
				<xsl:text>]</xsl:text>
			</xsl:when>
			<xsl:when test="@constant = 'yes'">
				<xsl:text> [constant]</xsl:text>
			</xsl:when>
			<xsl:when test="@value">
				<xsl:text> = </xsl:text>
				<xsl:value-of select="@value" />
			</xsl:when>
		</xsl:choose>

	</dt>
	<dd>
		<span class="var-description">
			<!-- description and notes -->
			<xsl:apply-templates select="." mode="var-description" />
		</span>
	</dd>
</xsl:template>

<!--
========== Variable offsets ("ats")
-->

<xsl:template match="*" mode="var-at">
	<xsl:choose>
		<xsl:when test="@at">
			<!-- Offset provided -->
			<code>
				<xsl:value-of select="@at" />
			</code>
			<xsl:text>: </xsl:text>
		</xsl:when>
		<xsl:otherwise>
			<!-- No offset provided (it might not be calculable) -->
			<xsl:text>[next]: </xsl:text>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>

<!--
========== Variable data types
-->

<!-- Simple data types -->
<xsl:template match="char | byte | word | dword | bit" mode="var-datatype">
	<!-- Data type name -->
	<xsl:value-of select="name()" />

	<!-- If it's enumerated, provide the appropriate link -->
	<xsl:if test="@enumeration">
		<xsl:text> (enum </xsl:text>
		<xsl:value-of select="@delimiter" />
		<xsl:call-template name="link-to-definition">
			<xsl:with-param name="type" select="'enumeration'" />
			<xsl:with-param name="name" select="@enumeration" />
			<xsl:with-param name="label" select="@enumeration" />
		</xsl:call-template>
		<xsl:text>)</xsl:text>
	</xsl:if>
</xsl:template>

<!-- Int: sizable numeric data type -->
<xsl:template match="int" mode="var-datatype">
	<!-- Output "int(size)" -->
	<xsl:text>int(</xsl:text>
	<xsl:call-template name="value-or-var-ref">
		<xsl:with-param name="value" select="@size" />
	</xsl:call-template>
	<xsl:text>)</xsl:text>
</xsl:template>

<!-- String: sizable (or delimited) character data type -->
<xsl:template match="string" mode="var-datatype">
	<xsl:text>string</xsl:text>

	<!-- Sized strings append a "(size)" -->
	<xsl:if test="@size">
		<xsl:text>(</xsl:text>
		<xsl:call-template name="value-or-var-ref">
			<xsl:with-param name="value" select="@size" />
		</xsl:call-template>
		<xsl:text>)</xsl:text>
	</xsl:if>

	<!-- If it's enumerated, provide the appropriate link -->
	<xsl:if test="@enumeration">
		<xsl:text> (enum </xsl:text>
		<xsl:value-of select="@delimiter" />
		<xsl:call-template name="link-to-definition">
			<xsl:with-param name="type" select="'enumeration'" />
			<xsl:with-param name="name" select="@enumeration" />
			<xsl:with-param name="label" select="@enumeration" />
		</xsl:call-template>
		<xsl:text>)</xsl:text>
	</xsl:if>

	<!-- Delimited strings must list the delimiter -->
	<xsl:if test="@delimiter">
		<xsl:text> (</xsl:text>
		<xsl:value-of select="@delimiter" />
		<xsl:text>-delimited)</xsl:text>
	</xsl:if>
</xsl:template>

<!-- Struct: reference to a structured data type -->
<xsl:template match="struct" mode="var-datatype">
	<xsl:text>struct </xsl:text>
	<xsl:call-template name="link-to-definition">
		<xsl:with-param name="type" select="'structdef'" />
		<xsl:with-param name="name" select="@type" />
		<xsl:with-param name="label" select="@type" />
	</xsl:call-template>

	<!-- indicate the size of this struct, if it is available -->
	<xsl:variable name="type">
		<xsl:value-of select="@type" />
	</xsl:variable>
	<xsl:variable name="lookup">
		<xsl:value-of select="/file/structdefs/structdef[@type = $type]/attribute::size" />
	</xsl:variable>
	<xsl:if test="$lookup">
		<span class="var-struct-size">
			<xsl:text> (</xsl:text>
			<xsl:if test="name(..) = 'array'">
					<xsl:text>each </xsl:text>
			</xsl:if>
			<xsl:text>size </xsl:text>
			<xsl:value-of select="$lookup" />
			<xsl:text>)</xsl:text>
		</span>
	</xsl:if>
</xsl:template>

<!-- Array: an ordered collection -->
<xsl:template match="array" mode="var-datatype">
	<xsl:text>array[ </xsl:text>

	<xsl:call-template name="value-or-var-ref">
		<xsl:with-param name="value" select="@size" />
	</xsl:call-template>

	<xsl:text> ] of </xsl:text>

	<xsl:apply-templates select="char|byte|word|dword|bit|int|string|struct|array|bitmask|unknown" mode="var-datatype" />
</xsl:template>

<!-- Bitmask: structured data type -->
<xsl:template match="bitmask" mode="var-datatype">
	<xsl:text>bitmask[</xsl:text>

	<xsl:call-template name="value-or-var-ref">
		<xsl:with-param name="value" select="@size" />
	</xsl:call-template>

	<xsl:text>]</xsl:text>
</xsl:template>

<!-- Unknown data type (number of bytes may be known, but the internal structure is not) -->
<xsl:template match="unknown" mode="var-datatype">
	<i>
		<xsl:text>unknown</xsl:text>
	</i>

	<xsl:text> (</xsl:text>
	<xsl:call-template name="value-or-var-ref">
		<xsl:with-param name="value" select="@size" />
	</xsl:call-template>
	<xsl:text> bytes)</xsl:text>
</xsl:template>

<!-- ====================================================================== -->

<!-- Variable names -->

<xsl:template match="*" mode="var-name">
	<xsl:if test="@name">
		<a name="variable-{@name}">
			<strong>
				<xsl:value-of select="@name" />
				<xsl:text>: </xsl:text>
			</strong>
		</a>
	</xsl:if>
</xsl:template>

<!-- ====================================================================== -->

<!-- Variable descriptions and notes -->

<xsl:template match="*" mode="var-description">
	<!-- Force the 'simple' view -->
	<xsl:apply-templates select="description" mode="simple" />

	<xsl:apply-templates select="notes" />

	<!-- arrays might have children with additional descriptions -->
	<xsl:if test="name() = 'array'">
		<xsl:apply-templates select="char|byte|word|dword|bit|int|string|struct|array|bitmask|unknown" mode="var-description" />
	</xsl:if>

	<!-- bitmasks have children that need to be listed -->
	<xsl:if test="name() = 'bitmask'">
		<xsl:apply-templates select="." mode="var-bitmask-contents" />
	</xsl:if>
</xsl:template>

<!-- ====================================================================== -->

<!-- Bitmask contents -->
<xsl:template match="bitmask" mode="var-bitmask-contents">
	<table class="bitmask-contents">
		<xsl:apply-templates select="bit" mode="var-bitmask-contents" />
	</table>
</xsl:template>

<xsl:template match="bit" mode="var-bitmask-contents">
	<tr>
		<td nowrap="nowrap">
			<xsl:text>bit </xsl:text>
			<xsl:value-of select="position()" />
			<xsl:text>:</xsl:text>
		</td>
		<td class="bit-name">
			<span class="var-name">
				<xsl:apply-templates select="." mode="var-name" />
			</span>

			<xsl:if test="@unknown = 'yes'">
				<em>
				<xsl:text>unknown </xsl:text>
				</em>
			</xsl:if>

			<!-- Output details about the value and whether it is constant or not -->
			<xsl:choose>
				<xsl:when test="@constant = 'yes' and @value">
					<xsl:text> [constant: </xsl:text>
					<xsl:value-of select="@value" />
					<xsl:text>]</xsl:text>
				</xsl:when>
				<xsl:when test="@constant = 'yes'">
					<xsl:text> [constant]</xsl:text>
				</xsl:when>
				<xsl:when test="@value">
					<xsl:text> = </xsl:text>
					<xsl:value-of select="@value" />
				</xsl:when>
			</xsl:choose>
		</td>

		<td class="bit-description">
			<!-- description and notes -->
			<xsl:apply-templates select="." mode="var-description" />
		</td>
	</tr>
</xsl:template>

<!-- ====================================================================== -->

<!--
========== Inline HTML content
-->

<!-- Any html content is output as-is, except with the 'html:' namespace removed -->
<xsl:template match="html:*">
	<xsl:element name="{local-name()}">
		<xsl:copy-of select="@*" />
		<xsl:apply-templates />
	</xsl:element>
</xsl:template>

<!-- ====================================================================== -->

<!--
========== Methods
-->

<!-- Display a decimal value, a hex value, or a reference to a variable -->
<xsl:template name="value-or-var-ref">
	<xsl:param name="value" />

	<!-- Find out what kind of value this is -->
	<xsl:choose>
		<!-- hex value -->
		<xsl:when test="starts-with( $value, '0x' )">
			<xsl:value-of select="$value" />
		</xsl:when>

		<!-- decimal value -->
		<xsl:when test="string( number( $value ) ) != 'NaN'">
			<xsl:value-of select="$value" />
		</xsl:when>

		<!-- relative offset -->
		<xsl:when test="starts-with( $value, '+' )">
			<xsl:value-of select="$value" />
		</xsl:when>

		<!-- variable reference -->
		<xsl:when test="starts-with( $value, '*' )">
			<!-- Determine if this is a local reference (structdef variable) or an absolute reference -->
			<xsl:variable name="ref_type">
				<xsl:choose>
					<xsl:when test="ancestor::*[structdef]">
						<xsl:text>member</xsl:text>
					</xsl:when>
					<xsl:otherwise>
						<xsl:text>variable</xsl:text>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:variable>

			<xsl:call-template name="link-to-definition">
				<xsl:with-param name="type" select="$ref_type" />
				<!-- The name is everything after the '*' -->
				<xsl:with-param name="name" select="substring( $value, 2 )" />
				<xsl:with-param name="label" select="substring( $value, 2 )" />
			</xsl:call-template>
		</xsl:when>

		<!-- unknown -->
		<xsl:otherwise>
			<em>
			<xsl:value-of select="$value" />
			</em>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>


<!-- Display a link to a variable definition -->
<xsl:template name="link-to-definition">
	<xsl:param name="filename" />
	<xsl:param name="type" />
	<xsl:param name="name" />
	<xsl:param name="label" />
	<xsl:param name="add-optional-file-link" />

	<!-- Construct the filename -->
	<xsl:variable name="fileref">

		<!-- If a file was specified, append a '.html' suffix -->
		<xsl:if test="$filename != ''">
			<xsl:value-of select="$filename" />
			<xsl:text>.html</xsl:text>
		</xsl:if>

		<!-- If a file wasn't specified, and it's an external structdef reference, look up the filename -->
		<xsl:if test="$filename = '' and $type = 'structdef'">
			<xsl:variable name="lookup">
				<xsl:value-of select="/file/structdefs/external-structdef[@type = $name]/attribute::file" />
			</xsl:variable>
			<xsl:if test="$lookup">
				<xsl:value-of select="$lookup" />
				<xsl:text>.html</xsl:text>
			</xsl:if>
		</xsl:if>

		<!-- If a file wasn't specified, and it's an external enumeration reference, look up the filename -->
		<xsl:if test="$filename = '' and $type = 'enumeration'">
			<xsl:variable name="lookup">
				<xsl:value-of select="/file/enumerations/external-enumeration[@type = $name]/attribute::file" />
			</xsl:variable>
			<xsl:if test="$lookup">
				<xsl:value-of select="$lookup" />
				<xsl:text>.html</xsl:text>
			</xsl:if>
		</xsl:if>
	</xsl:variable>

	<!-- Construct the display label -->
	<xsl:variable name="display_label">
		<xsl:choose>
			<!-- Preference: label, then name, then the filename, then static text '[link]' -->
			<xsl:when test="$label != ''">
				<xsl:value-of select="$label" />
			</xsl:when>
			<xsl:when test="$name != ''">
				<xsl:value-of select="$name" />
			</xsl:when>
			<xsl:when test="$filename != ''">
				<xsl:value-of select="$filename" />
			</xsl:when>
			<xsl:otherwise>
				<xsl:text>[link]</xsl:text>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:variable>

	<!-- Create a link based on whatever information was passed in -->
	<xsl:element name="a">
		<!-- the link (href) -->
		<xsl:attribute name="href">
			<xsl:value-of select="$fileref" />

			<!-- If type and name are given, it's a reference to a specific variable -->
			<xsl:if test="($type != '') and ($name != '')">
				<xsl:text>#</xsl:text>
				<xsl:value-of select="$type" />
				<xsl:text>-</xsl:text>
				<xsl:value-of select="$name" />
			</xsl:if>
		</xsl:attribute>

		<!-- if it's an external reference, flag that with a style -->
		<xsl:if test="$fileref != ''">
			<xsl:attribute name="class">
				<xsl:text>external</xsl:text>
			</xsl:attribute>
		</xsl:if>

		<!-- the label -->
		<xsl:value-of select="$display_label" />
	</xsl:element>

	<!-- If asked for, and it's a reference within another file, add a plain link to the file itself -->
	<xsl:if test="$add-optional-file-link != ''">
		<xsl:if test="($filename != '') and ($type != '') and ($name != '')">
			<xsl:text> (found in </xsl:text>
			<xsl:call-template name="link-to-definition">
				<xsl:with-param name="filename" select="$filename" />
				<xsl:with-param name="label" select="$filename" />
			</xsl:call-template>
			<xsl:text>)</xsl:text>
		</xsl:if>
	</xsl:if>
</xsl:template>

</xsl:transform>