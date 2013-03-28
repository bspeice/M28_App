from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string
import os
import codecs

class Command(BaseCommand):

	args = '<full_path_to_render>'
	help = 'Renders the templates found in <APP_DIR>/pages to either the supplied path or <APP_DIR>/dist'

	def handle(self, *args, **options):
		import M28 #Application
		APP_DIR = M28.__path__[0]

		# Allow this to be an option later maybe?
		IN_DIR = os.path.join(APP_DIR, 'pages')

		if len(args) > 0:
			OUT_DIR = args[0]
		else:
			OUT_DIR = os.path.join(APP_DIR, 'dist')

		# Verify the IN_DIR is sane
		if os.path.exists(IN_DIR):
			if not os.path.isdir(IN_DIR):
				raise CommandError("Could not open the 'pages' directory for rendering the templates!\n")
		else:
			os.mkdir(IN_DIR)
			raise CommandError("The pages directory didn't exist! I've created one for you. Put your pages there.")

		# Verify the OUT_DIR is sane
		if os.path.exists(OUT_DIR):
			if not os.path.isdir(OUT_DIR):
				raise CommandError("Could not open the 'dist' directory for rendering the templates!\n")
		else:
			os.mkdir(OUT_DIR)
			self.stderr.write("The 'dist' directory didn't exist! I've created it for you and I'm about to fill it up.")

		# Now we're ready to start going!
		for (root, directories, files) in os.walk(IN_DIR):
			for file in files:
				full_path = os.path.join(root, file)
				self.stdout.write("Rendering file %s..." % file)

				utf8_template_string = render_to_string(file)

				out_path = os.path.join(OUT_DIR, file)
				codecs.open(out_path, 'w', 'utf8').write(utf8_template_string)
