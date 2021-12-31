$( document ).ready( function(){
    //all events should be in here
    //dom critical functions here

    /******************************************************************************/
	/*******************************Modal Events***********************************/
	/******************************************************************************/
	//$(document).on(event, selector, handler).
	//bind to future event
	//default close x option
	$( document ).on( 'click', '.modal .close', function () {
		var modal = $( this ).closest( '.modal' );
		var id = $( modal ).attr( 'data-id' );
		closeModal( modal );
	} );

	//modal button events
	$( document ).on( 'click', '.modal input[type=button]', function () {
		var modal = $( this ).closest( '.modal' );
		var id = $( modal ).attr( 'data-id' );
		//get data for modal
		var data = window.modals.data[id].buttons;
		for ( i = 0; i < data.length; i++ ) {
			if ( data[i].value == $( this ).attr( 'value' ) ) {
				//run the onclick
				var cleanExit = true;
				if ( data[i].onclick ) {
					cleanExit = data[i].onclick( id );
				}
				if ( cleanExit ) {
					closeModal( $( modal ) );
				}
			}
		}
	} );

	//modal esc key event
	$( document ).on( 'keyup', function ( e ) {
		if ( window.modals.displaying ) {
			if ( e.keyCode == 27 ) {
				if( !window.modals.data[window.modals.displaying].noExit ) {
					closeModal( $( '.modal[data-id=' + window.modals.displaying + ']' ) );
				}
			}
		}
	} );

	//modal reposition after resize
	$( window ).on( 'resize', function () {
		$( '.modal' ).each( function ( idx, elem ) {
			$( elem ).css( 'left', ( $( 'body' ).width() / 2 ) - ( $( elem ).width() / 2 ) + 'px' );
		} );
	} );

	//modal shadow click
	$( document ).on( 'click', '.modalShadow', function () {
		//check the data on it to make sure there is no override for this option
		var id = $( this ).attr( 'data-id' );
		var modal = window.modals.data[id];
		if ( modal.shadowClose ) {
			if ( isset( modal.shadowPrompt ) ) {
				confirmModal( modal.shadowPrompt, function () {
					closeModalId( id );
					return true
				}, undefined );
			} else {
				closeModalId( id );
			}
		}
	} );
});

//util functions here
window.modals = { ids: new Set(), data: {}, displaying: false };
/**
 * options structure
 * {
 *  title: "string", //the header for the title
 *  footer: true, //has a footer [optional]
 *  shadowClose: true, //clicking the shadow closes the modal [optional]
 *  shadowPrompt: "", //prompt for the user to close [optional]
 *  buttons: [ //buttons for footer
 *  	0 : {
 *  		value : "string", //value of the button
 *			name : "string", //name of the input [optional]
 *  		onclick : function, //click event to run [optional]
 *  		class : "string" //class of the button for style or whatever [optional]
 *  		focus : true //focus on this button [optional],
 *  		disabled : true //button will be disabled [optional]
 *  	}
 *  ]
 * @param options
 */
function createModal( options ) {
	var id = 0;
	if ( window.modals.ids.length == 0 ) {
		id = 1;
	} else {
		id = window.modals.ids.peek() + 1;
	}

	if ( !isset( options['shadowClose'] ) ) {
		options['shadowClose'] = true;
	}

	if ( !isset( options['noExit'] ) ) {
		options['noExit'] = false;
	}

	if ( !isset( options['focus'] ) ) {
		options['focus'] = false;
	}

	if( !isset( options['wide'] ) ){
		options['wide'] = false;
	}

	var zIndex = ' style="z-index: ' + ( 10 + ( id - 1 ) ) + '" ';
	var html = '<div data-id="' + id + '" class="modal none"' + zIndex + '>' +
		'<div class="modalWrapper' + ( options['wide'] ? ' wide' : '' )+ '">';
	if ( options.title ) { //insert the header
		html += '<div class="modalHeaderWrapper"><div class="modalHeader clearfix">' +
			'<span class="title">' + options.title + '</span>';
		if( !options['noExit'] ) {
			html += '<span class="close">&times;</span>';
		}
			html += '</div></div>';
	}
	//insert the content section
	html += '<div class="modalContentWrapper"><div class="modalContent"></div></div>';

	if ( options.footer || options.buttons ) { //insert the header
		html += '<div class="modalFooterWrapper"><div class="modalFooter">';
		if ( options.buttons ) {
			for ( i = 0; i < options.buttons.length; i++ ) {
				var x = options.buttons[i];
				x.class = x.class ? x.class : '';
				x.name = x.name ? x.name : '';
				html += "<input " +
					"type='button' " +
					"value='" + x.value + "' " +
					"class='" + x.class + "' " +
					"name='" + x.name + "' " +
					( ( x.disabled ) ? ( "disabled=disabled" ) : ( '' ) ) +
					( ( x.focus ) ? 'autofocus />' : '/>' );
			}
		}
		html += '</div></div>';
	}
	$( 'body' ).append( '<div class="modalShadow none" data-id="' + id + '"' + zIndex + '>&nbsp;</div>' ).append( html );
	window.modals.data[id] = options;
	window.modals.ids.push( id );
	return $( '.modal[data-id=' + id + ']' );
}

function setModalContent( modal, html ) {
	$( modal ).find( '.modalContent' ).html( html );
}

function setModalContentAjax( modal, url, data, onSuccess ) {
	if( !isset( data ) ) data = null;
	setModalContent( modal, '<div class=margin10>'+ajaxLoaderBars( 10 )+'</div>' );
	$.post( url, data, function( d ){
		setModalContent( modal, d );
		if( isset( onSuccess ) ) {
			onSuccess();
		}
	});
}

function appendModalContent( modal, html ) {
	$( modal ).find( '.modalContent' ).append( html );
}

function appendModalContent( modal, html ) {
	$( modal ).find( '.modalContent' ).html( $( modal ).find( '.modalContent' ).html() + html );
}

function displayModal( modal, focusIndex ) {
	//center the modal on the screen
	var id = $( modal ).attr( 'data-id' );
	$( modal ).css( 'left', ( $( 'body' ).width() / 2 ) - ( $( modal ).width() / 2 ) + 'px' );
	$( modal ).css( 'top', ( $( document ).scrollTop() ) + 'px' );
	$( '.modalShadow[data-id=' + id + ']' ).fadeIn( 300 );
	$( modal ).fadeIn( 300 );
	//find focus if any exist
	var data = window.modals.data[id];
	if( data.buttons ) {
		for ( var i = 0; i < data.buttons.length; i++ ) {
			if ( data.buttons[i].focus ) {
				$( '.modal[data-id=' + id + '] input[name="' + data.buttons[i].name + '"]' ).focus();
				$( '.modal[data-id=' + id + '] input[value="' + data.buttons[i].value + '"]' ).focus();
			}
		}
	}
	//$('html, body').animate({
	//	scrollTop: $( modal ).offset().top
	//}, 200);
	//autoload select2 if present
	window.modals.displaying = $( modal ).attr( 'data-id' );
}

function closeModalId( id ) {
	var modal = $( '.modal[data-id=' + id + ']' );
	delete window.modals.data[id];
	window.modals.ids.pop( id );
	if ( $( '.modal:not([data-id=' + id + '])' ).last().length ) {
		window.modals.displaying = $( '.modal' ).last().attr( 'data-id' );
	} else {
		window.modals.displaying = false;
	}
	$( modal ).fadeOut( 300, function () {
		$( modal ).remove();
	} );
	$( '.modalShadow[data-id=' + id + ']' ).fadeOut( 300, function () {
		$( this ).remove();
	} );
}

function closeModal( modal ) {
	//modal.find( '.modalWrapper' ).hide();
	var id = $( modal ).attr( 'data-id' );
	delete window.modals.data[id];
	window.modals.ids.pop( id );
	if ( $( '.modal:not([data-id=' + id + '])' ).last().length ) {
		window.modals.displaying = $( '.modal' ).last().attr( 'data-id' );
	} else {
		window.modals.displaying = false;
	}
	$( modal ).fadeOut( 300, function () {
		$( modal ).remove();
	} );
	$( '.modalShadow[data-id=' + id + ']' ).fadeOut( 300, function () {
		$( this ).remove();
	} );
}

function confirmModal( question, yesAction, noAction ) {
	var modal = createModal( {
		title: "Confirm",
		buttons: [
			{
				value: "Yes",
				onclick: yesAction
			},
			{
				value: "Cancel",
				onclick: noAction,
				class: 'redGlow'
			}
		]
	} );
	setModalContent( modal, question );
	displayModal( modal );
	//$( modal ).effect( 'shake' );
}

function errorModal( message, ut ) {
	var title = isset( ut ) ? ut : "Error";
	messageModal( message, title, true );
}

function messageModal( message, ut, error, action, shadowClose ) {
	error = isset( error ) ? error : false;
	var title = isset( ut ) ? ut : "Message";
	var struct = {
		title: title,
		buttons: [
			{
				value: "Ok",
				focus: true
			}
		]
	};
	if( typeof shadowClose !== "undefined" ){
		struct.shadowClose = shadowClose;
	}
	if( typeof action === "function" ){
		struct.buttons[0].onclick = action;
	}
	var modal = createModal( struct );
	setModalContent( modal, message );
	displayModal( modal );
	// if ( error )
	// 	$( modal ).effect( 'shake' );
}

function messageModalAjax( ajax, title, error, action, shadowClose ){
	error = isset( error ) ? error : false;
	var ut = isset( title ) ? title : "Message";
	var struct = {
		title: ut,
		buttons: [
			{
				value: "Ok",
				focus: true
			}
		]
	};
	if( typeof shadowClose !== "undefined" ){
		struct.shadowClose = shadowClose;
	}
	if( typeof action === "function" ){
		struct.buttons[0].onclick = action;
	}
	var modal = createModal( struct );
	setModalContentAjax( modal, ajax );
	displayModal( modal );
	// if ( error )
	// 	$( modal ).effect( 'shake' );
}

function isset( value ) {
	if ( typeof value !== 'undefined' ) {
		return true;
	}
	return false;
}

function log( ...x ){
	console.log( x )
}